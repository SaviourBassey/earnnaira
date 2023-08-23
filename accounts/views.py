from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CouponCode, UserAdditionalInformation, Vendor

# Create your views here.

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
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
                            UserAdditionalInformation.objects.create(user=user, phone=phone)
                            return redirect("accounts:login_view")
                        else:
                            messages.error(request, "Wrong Coupon Code")
                            return redirect("accounts:register_view")
                    else:
                        messages.error(request, "Password do not match")
                        return redirect("accounts:register_view")
                else:
                    messages.error(request, "Password must contain atleast 1 Uppercase, 1 lowercase, 1 digit and a special character and at least 8 characters long")
                    return redirect("accounts:register_view")
            else:
                messages.error(request, "Password too short. Your password must contain at least 8 characters.")
                return redirect("accounts:register_view")


class SignInView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, "accounts/login.html")

    def post(self, request, *args, **kwargs):
        username = str(request.POST.get("username")).lower()
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            fetch_user = User.objects.filter(username=username)[0]
            username = fetch_user.username
            user = authenticate(request, username=username, password=password)
            if user is not None:
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
        logout(request)
        all_vendors = Vendor.objects.all()
        context = {
            "all_vendors":all_vendors
        }
        return render(request, "accounts/vendor.html", context)