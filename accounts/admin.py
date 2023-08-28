from django.contrib import admin
from .models import Vendor, CouponCode, UserAdditionalInformation, DailyLoginReward, ReferalReward, Referral

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor_whatsapp_number",)
    search_fields = ("vendor_whatsapp_number",)
admin.site.register(Vendor, VendorAdmin)


class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ("generated_by", "used_by", "active")
    list_filter = ("generated_by",)
    search_fields = ("coupon_code",)
admin.site.register(CouponCode, CouponCodeAdmin)


class UserAdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "referral_link")
    search_fields = ("phone", "user",)
admin.site.register(UserAdditionalInformation, UserAdditionalInformationAdmin)


class DailyLoginRewardAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_login_bal",)
admin.site.register(DailyLoginReward, DailyLoginRewardAdmin)


class ReferalRewardAdmin(admin.ModelAdmin):
    list_display = ("user", "direct_bal", "indirect_bal", "second_indirect_bal", "total_bal")
    list_filter = ("direct_bal", "indirect_bal", "second_indirect_bal")
admin.site.register(ReferalReward, ReferalRewardAdmin)


class ReferralAdmin(admin.ModelAdmin):
    list_display = ("referring_user", "referred_user",)
    list_filter = ("referring_user",)
admin.site.register(Referral, ReferralAdmin)