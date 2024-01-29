from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from ..serializers import CustomUserSerializer, OTPSerializer
from dotenv import load_dotenv
from datetime import datetime, timedelta
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
            user = user_serializer.save()
            otp_code = self.generate_otp()
            hashed_otp = self.hash_otp(otp_code)
            expiration_time = datetime.now() + timedelta(minutes=15)
            
            otp_data = {'user': user.id, 'OTP': hashed_otp, 'expiration_time': expiration_time}
            otp_serializer = OTPSerializer(data=otp_data)
            if otp_serializer.is_valid():
                otp_serializer.save()
                self.send_otp_email(user.email, otp_code)
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            return Response(otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)