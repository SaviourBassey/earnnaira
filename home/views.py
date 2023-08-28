from django.shortcuts import render
from django.views import View
from accounts.models import UserAdditionalInformation

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home/index.html")
    

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home/about_us.html")
    
class TopEarnerView(View):
    def get(self, request, *args, **kwargs):
        top_earners = UserAdditionalInformation.objects.all().order_by("-account_bal")[:15]
        context = {
            "top_earners":top_earners
        }
        return render(request, "home/top-earner.html", context)