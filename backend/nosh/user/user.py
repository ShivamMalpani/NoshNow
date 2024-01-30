from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone as dj_timezone
from ..models import CustomUser, OTP
from ..serializers import CustomUserSerializer, OTPSerializer, UserLoginSerializer
from dotenv import load_dotenv
from datetime import timedelta
from hashlib import sha256
import random
import os


load_dotenv()


class RegistrationView(APIView):
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    def hash_otp(self, otp):
        return sha256(otp.encode()).hexdigest()
    
    def send_otp_email(self, email, otp):
        subject = 'Your OTP for Registration'
        message = f'Your OTP is: {otp}. Please use it to complete the registration process.'
        send_mail(subject, message, os.getenv("EMAIL"), [email])

    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            user = user_serializer.save()
            otp_code = self.generate_otp()
            hashed_otp = self.hash_otp(otp_code)
            expiration_time = dj_timezone.now() + timedelta(minutes=5)
            
            otp_data = {'user': user.id, 'OTP': hashed_otp, 'expiration_time': expiration_time}
            otp_serializer = OTPSerializer(data=otp_data)
            if otp_serializer.is_valid():
                otp_serializer.save()
                self.send_otp_email(user.email, otp_code)
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            return Response(otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailOTP(APIView):
    def post(self, request):
        email = self.request.data.get("email")
        otp = self.request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response("User not found, please register first", status=status.HTTP_404_NOT_FOUND)
        
        if user.email_verified == True:
            return Response("User already verified", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            otp_instance = OTP.objects.get(user=user.id)
        except:
            return Response("OTP not found please request another OTP", status=status.HTTP_404_NOT_FOUND)
        
        time_now = dj_timezone.now()
        if otp_instance.expiration_time < time_now:
            otp_instance.delete()
            return Response("OTP expired request another one", status=status.HTTP_400_BAD_REQUEST)
        
        hashed_otp = sha256(otp.encode()).hexdigest()
        if hashed_otp != otp_instance.OTP:
            return Response("Incorrect OTP", status=status.HTTP_400_BAD_REQUEST)
        
        user.email_verified = True
        user.save()
        otp_instance.delete()
        return Response("OTP verified successfully", status=status.HTTP_200_OK)


class SendEmailOtpView(APIView):
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    def hash_otp(self, otp):
        return sha256(otp.encode()).hexdigest()
    
    def send_otp_email(self, email, otp):
        subject = 'Your OTP for Registration'
        message = f'Your OTP is: {otp}. Please use it to complete the registration process.'
        send_mail(subject, message, os.getenv("EMAIL"), [email])

    def post(self, request):
        email = self.request.data.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response("User not found, please register first", status=status.HTTP_404_NOT_FOUND)
        
        if user.email_verified == True:
            return Response("User already verified", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            otp_instance = OTP.objects.get(user=user.id)
            time_now = dj_timezone.now()
            if otp_instance.expiration_time > time_now:
                return Response("OTP is already active, please wait", status=status.HTTP_400_BAD_REQUEST)
            otp_instance.delete()
        except OTP.DoesNotExist:
            pass

        otp_code = self.generate_otp()
        hashed_otp = self.hash_otp(otp_code)
        expiration_time = dj_timezone.now() + timedelta(minutes=5)

        otp_data = {'user': user.id, 'OTP': hashed_otp, 'expiration_time': expiration_time}
        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()
            self.send_otp_email(user.email, otp_code)
            return Response("OTP sent", status=status.HTTP_200_OK)
        return Response(otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)