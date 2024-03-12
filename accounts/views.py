from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CouponCode, UserAdditionalInformation, Vendor, Referral, ReferalReward
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse

# Create your views here.

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        referral_user = request.GET.get('ref')
        if referral_user:
            context = {
                "referral_user":referral_user
            }
            return render(request, "accounts/register.html", context)
        
        return render(request, "accounts/register.html")

    def post (self, request, *args, **kargs):
        first_name = str(request.POST.get('first_name')).lower()
        last_name = str(request.POST.get('last_name')).lower()
        phone = request.POST.get('phone')
        email = str(request.POST.get('email')).lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = str(request.POST.get('username')).lower()
        coupon_code = str(request.POST.get('coupon_code'))
        referral_user = str(request.POST.get('referral_user')).lower()
        if User.objects.filter(username=username).exists():
            messages.error(request, "An account with the username already exist")
            return redirect("accounts:register")
        else:
            if len(password1) > 7:
                l, u, s, d = 0, 0, 0, 0
                for i in password1:
                    if (i.islower()):
                        l += 1
                    if (i.isupper()):
                        u += 1
                    if (i.isdigit()):
                        d += 1
                    if (i=="!" or i=="@" or i=="#" or i=="$" or i=="%" or i=="^" or i=="&" or i=="*" or i=="(" or i==")" or i=="-" or i=="_" or i=="+" or i=="=" or i=="{" or i=="}" or i=="[" or i=="]" or i=="|" or i=="\\" or i=="<" or i==">" or i=="?" or i=="/"):
                        s += 1
                print(l, u, s, d, l+s+u+d, len(password1))
                if (l>=1 and u>=1 and s>=1 and d>=1 and l+s+u+d==len(password1)):
                    if password1 == password2:
                        if CouponCode.objects.filter(coupon_code=coupon_code, active=True, used_by=None).exists():
                            user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                            additional_info = UserAdditionalInformation.objects.get(user=user)
                            additional_info.phone = phone
                            additional_info.activity_bal = additional_info.activity_bal + 2000
                            additional_info.referral_link = request.build_absolute_uri(reverse('accounts:register_view')) + f'?ref={user.username}'
                            additional_info.save()

                            cp = CouponCode.objects.filter(coupon_code=coupon_code, active=True, used_by=None).first()
                            cp.active = False
                            cp.used_by = user
                            cp.save()

                            #implementing Referal Sysytem
                            '''
                            referral_user is the user whose referral link is been used
                            indirect_referer_user is the user ...
                            '''
                            if referral_user:
                                if User.objects.filter(username=referral_user).exists():
                                    referring_user_objects = User.objects.get(username=referral_user)
                                    Referral.objects.create(referring_user=referring_user_objects, referred_user=user, generation=1)
                                    direct_referer_reward = ReferalReward.objects.get(user=referring_user_objects)
                                    direct_referer_reward.direct_bal = direct_referer_reward.direct_bal + 1500
                                    direct_referer_reward.save()
                                    additional_info = UserAdditionalInformation.objects.get(user=referring_user_objects)
                                    additional_info.account_bal = additional_info.account_bal + 1500
                                    additional_info.save()

                                    if Referral.objects.filter(referred_user=referring_user_objects).exists():
                                        indirect_referer = Referral.objects.get(referred_user=referring_user_objects)
                                        indirect_referer_user = indirect_referer.referring_user
                                        indirect_referer_reward = ReferalReward.objects.get(user=indirect_referer_user)
                                        indirect_referer_reward.indirect_bal = indirect_referer_reward.indirect_bal + 200
                                        indirect_referer_reward.save()
                                        additional_info = UserAdditionalInformation.objects.get(user=indirect_referer_user)
                                        additional_info.account_bal = additional_info.account_bal + 200
                                        additional_info.save()

                                        if Referral.objects.filter(referred_user=indirect_referer_user).exists():
                                            second_indirect_referer = Referral.objects.get(referred_user=indirect_referer_user)
                                            second_indirect_referer_user = second_indirect_referer.referring_user
                                            second_indirect_referer_reward = ReferalReward.objects.get(user=second_indirect_referer_user)
                                            second_indirect_referer_reward.second_indirect_bal = second_indirect_referer_reward.second_indirect_bal + 100
                                            second_indirect_referer_reward.save()
                                            additional_info = UserAdditionalInformation.objects.get(user=second_indirect_referer_user)
                                            additional_info.account_bal = additional_info.account_bal + 100
                                            additional_info.save()

                            return redirect("accounts:login_view")
                        else:
                            messages.error(request, "Wrong Coupon Code")
                            if referral_user:
                                return redirect(request.build_absolute_uri(reverse('accounts:register_view')) + f'?ref={referral_user}')
                            else:
                                return redirect("accounts:register_view")
                    else:
                        messages.error(request, "Password do not match")
                        if referral_user:
                            return redirect(request.build_absolute_uri(reverse('accounts:register_view')) + f'?ref={referral_user}')
                        else:
                            return redirect("accounts:register_view")
                else:
                    messages.error(request, "Password must contain atleast 1 Uppercase, 1 lowercase, 1 digit and a special character and at least 8 characters long")
                    if referral_user:
                        return redirect(request.build_absolute_uri(reverse('accounts:register_view')) + f'?ref={referral_user}')
                    else:
                        return redirect("accounts:register_view")
            else:
                messages.error(request, "Password too short. Your password must contain at least 8 characters.")
                if referral_user:
                    return redirect(request.build_absolute_uri(reverse('accounts:register_view')) + f'?ref={referral_user}')
                else:
                    return redirect("accounts:register_view")


class SignInView(View):
    def get(self, request, *args, **kwargs):
        #print(User.objects.all())
        # logout(request)
        return render(request, "accounts/login.html")

    def post(self, request, *args, **kwargs):
        username = str(request.POST.get("username")).lower()
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            fetch_user = User.objects.filter(username=username)[0]
            username = fetch_user.username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Implementing the daily login reward
                today = timezone.now().date()
                last_login = user.last_login
                if last_login:
                    last_login = user.last_login.date()
                    if last_login < today:
                        try:
                            daily_reward = UserAdditionalInformation.objects.get(user=user)
                            daily_reward.activity_bal = daily_reward.activity_bal + 200
                            daily_reward.save()
                        except:
                            pass
                else:
                    try:
                        daily_reward = UserAdditionalInformation.objects.get(user=user)
                        daily_reward.activity_bal = daily_reward.activity_bal + 200
                        daily_reward.save()
                    except:
                        pass

                login(request, user)
                return redirect("dashboard:my_accounts_view")
            else:
                messages.error(request, "Incorrect Credentials, please check your login details again")
                return redirect("accounts:login_view")
        else:
            messages.error(request, "Username not recognized")
            return redirect("accounts:login_view")


class VendorView(View):
    def get(self, request, *args, **kwargs):
        # logout(request)
        all_vendors = Vendor.objects.all()
        context = {
            "all_vendors":all_vendors
        }
        return render(request, "accounts/vendor.html", context)
    


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("home:home_view")