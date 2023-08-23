from django.contrib import admin
from .models import Vendor, CouponCode, UserAdditionalInformation

# Register your models here.

admin.site.register(Vendor)

admin.site.register(CouponCode)

admin.site.register(UserAdditionalInformation)