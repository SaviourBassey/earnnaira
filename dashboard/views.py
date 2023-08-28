from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Referral

# Create your views here.

class MyAccountView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/my_account.html")
    

class RequestPaymentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/payment_request.html")
    

class ReferralView(View):
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