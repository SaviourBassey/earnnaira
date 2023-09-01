from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Referral, UserAdditionalInformation
from django.contrib import messages
from .models import PaymentRequest
from django.utils import timezone

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
        # Get the current date and time in the timezone specified in your Django settings
        current_datetime = timezone.now()

        if current_datetime.weekday() == 0:
            # Set the timezone for your target time range (1pm to 3pm)
            #start_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 13, 0, 0))
            #end_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 15, 0, 0))

            start_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 13, 0, 0))
            end_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 19, 0, 0))

            # Check if the current time is between 1pm and 3pm (inclusive)
            if start_time <= current_datetime <= end_time:
                if withdrawal_amount <= account_balance:
                    print(withdrawal_amount)
                    if withdrawal_amount >= 6000:
                        if description:
                            user_bal = UserAdditionalInformation.objects.get(user=request.user)
                            print(user_bal)
                            user_bal.account_bal = user_bal.account_bal - withdrawal_amount
                            print(user_bal)
                            user_bal.save()
                            PaymentRequest.objects.create(user=request.user, request_status="PENDING", description=description, amount=withdrawal_amount, bank_name=bank_name, account_number=account_number)
                        else:
                            user_bal = UserAdditionalInformation.objects.get(user=request.user)
                            print(user_bal)
                            user_bal.account_bal = user_bal.account_bal - withdrawal_amount
                            print(user_bal)
                            user_bal.save()
                            PaymentRequest.objects.create(user=request.user, request_status="PENDING", amount=withdrawal_amount, bank_name=bank_name, account_number=account_number)

                        messages.success(request, "Withdrawal Placed Successfully")
                        return redirect("dashboard:request_payment_view")
                    else:
                        messages.error(request, "Withdrawal Amount must be from N6000 and above")
                        return redirect("dashboard:request_payment_view")
                else:
                    messages.error(request, "Insufficient Account Balance")
                    return redirect("dashboard:request_payment_view")
            else:
                messages.error(request, "Withdrawal starts from 1pm")
                return redirect("dashboard:request_payment_view")
        elif current_datetime.weekday() == 4:
            # Set the timezone for your target time range (1pm to 3pm)
            #start_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 13, 0, 0))
            #end_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 15, 0, 0))

            start_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 13, 0, 0))
            end_time = timezone.make_aware(timezone.datetime(current_datetime.year, current_datetime.month, current_datetime.day, 19, 0, 0))

            # Check if the current time is between 1pm and 3pm (inclusive)
            if start_time <= current_datetime <= end_time:
                if withdrawal_amount <= account_balance:
                    if withdrawal_amount >= 6000:
                        if description:
                            user_bal = UserAdditionalInformation.objects.get(user=request.user)
                            print(user_bal)
                            user_bal.account_bal = user_bal.account_bal - withdrawal_amount
                            print(user_bal)
                            user_bal.save()
                            PaymentRequest.objects.create(user=request.user, request_status="PENDING", description=description, amount=withdrawal_amount, bank_name=bank_name, account_number=account_number)
                        else:
                            user_bal = UserAdditionalInformation.objects.get(user=request.user)
                            print(user_bal)
                            user_bal.account_bal = user_bal.account_bal - withdrawal_amount
                            print(user_bal)
                            user_bal.save()
                            PaymentRequest.objects.create(user=request.user, request_status="PENDING", amount=withdrawal_amount, bank_name=bank_name, account_number=account_number)

                        messages.success(request, "Withdrawal Placed Successfully")
                        return redirect("dashboard:request_payment_view")
                    else:
                        messages.error(request, "Withdrawal Amount must be from N6000 and above")
                        return redirect("dashboard:request_payment_view")
                else:
                    messages.error(request, "Insufficient Account Balance")
                    return redirect("dashboard:request_payment_view")
            else:
                messages.error(request, "Withdrawal starts from 1pm")
                return redirect("dashboard:request_payment_view")
        else:
            messages.error(request, "Withdrawal is only on Mondays and Fridays from 1pm - 3pm")
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
    

class SpinAndWinView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/spin_and_win.html")