from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(UserMod)
admin.site.register(PaymentHistory)

# Register your models here.
