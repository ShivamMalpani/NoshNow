from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(CustomUser, UserAdmin)
admin.site.register(OTP)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(UserMod)
admin.site.register(PaymentHistory)

# Register your models here.
