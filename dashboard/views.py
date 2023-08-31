from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Referral, UserAdditionalInformation
from django.contrib import messages
from .models import PaymentRequest

# Create your views here.

class MyAccountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        direct = 0
        indirect = 0
        second_direct_referer = 0
        #1st generation
        if Referral.objects.filter(referring_user=request.user, generation=1).exists():
            direct = Referral.objects.filter(referring_user=request.user, generation=1).count()

            #2nd generation
            for i in Referral.objects.filter(referring_user=request.user, generation=1):
                if Referral.objects.filter(referring_user=i.referred_user).exists():
                    indirect = Referral.objects.filter(referring_user=i.referred_user).count()

                    #3rd generation
                    for j in Referral.objects.filter(referring_user=i.referred_user):
                        if Referral.objects.filter(referring_user=j.referred_user).exists():
                            second_direct_referer = Referral.objects.filter(referring_user=j.referred_user).count()

        withdrawal_transaction = PaymentRequest.objects.filter(user=request.user)
        first_5_transaction = withdrawal_transaction.order_by("-timestamp")[:5]
        context = {
            "direct":direct,
            "indirect":indirect,
            "second_direct_referer": second_direct_referer,
            "first_5_transaction":first_5_transaction
        }
        return render(request, "dashboard/my_account.html", context)
    

class RequestPaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        account_bal = UserAdditionalInformation.objects.get(user=request.user)
        context = {
            "account_bal":account_bal
        }
        return render(request, "dashboard/payment_request.html", context)
    
    def post(self, request, *args, **kwargs):
        bank_name = str(request.POST.get('bank_name')).lower()
        description = str(request.POST.get('description')).lower()
        account_balance = int(request.POST.get('account_balance'))
        account_number = int(request.POST.get('account_number'))
        withdrawal_amount = int(request.POST.get('withdrawal_amount'))
        if withdrawal_amount <= account_balance:
            if description:
                PaymentRequest.objects.create(user=request.user, request_status="PENDING", description=description, amount=withdrawal_amount, bank_name=bank_name, account_number=account_number)
            else:
                PaymentRequest.objects.create(user=request.user, request_status="PENDING", amount=withdrawal_amount, bank_name=bank_name, account_number=account_number)

            messages.success(request, "Withdrawal Placed Successfully")
            return redirect("dashboard:request_payment_view")
        else:
            messages.error(request, "Insufficient Account Balance")
            return redirect("dashboard:request_payment_view")
    

class ReferralView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        direct = 0
        indirect = 0
        second_direct_referer = 0
        first_gen_list = Referral.objects.none()
        second_gen_list = Referral.objects.none()
        third_gen_list = Referral.objects.none()
        merged_queryset = Referral.objects.none()
        #1st generation
        if Referral.objects.filter(referring_user=request.user, generation=1).exists():
            first_gen_list = Referral.objects.filter(referring_user=request.user, generation=1)
            direct = Referral.objects.filter(referring_user=request.user, generation=1).count()

            #2nd generation
            for i in Referral.objects.filter(referring_user=request.user, generation=1):
                if Referral.objects.filter(referring_user=i.referred_user).exists():
                    second_gen_list = Referral.objects.filter(referring_user=i.referred_user)
                    indirect = Referral.objects.filter(referring_user=i.referred_user).count()

                    #3rd generation
                    for j in Referral.objects.filter(referring_user=i.referred_user):
                        if Referral.objects.filter(referring_user=j.referred_user).exists():
                            third_gen_list = Referral.objects.filter(referring_user=j.referred_user)
                            second_direct_referer = Referral.objects.filter(referring_user=j.referred_user).count()

        merged_queryset = first_gen_list | second_gen_list | third_gen_list
        sorted_queryset = merged_queryset.order_by('-timestamp')

        context = {
            "direct":direct,
            "indirect":indirect,
            "second_direct_referer": second_direct_referer,
            "total_referrals": direct + indirect + second_direct_referer,
            "first_gen_list": first_gen_list,
            "second_gen_list": second_gen_list,
            "third_gen_list": third_gen_list,
            "sorted_queryset": sorted_queryset
        }
        return render(request, "dashboard/referrals.html", context)