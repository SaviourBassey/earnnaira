from django.contrib import admin
from .models import PaymentRequest, Spin

# Register your models here.

class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_id", "request_status", "amount")
    list_filter = ("request_status",)
    search_fields = ("transaction_id",)
admin.site.register(PaymentRequest, PaymentRequestAdmin)


admin.site.register(Spin)