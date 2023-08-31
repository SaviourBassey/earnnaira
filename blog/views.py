from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PostCategory, Post, PostShare
from django.http import JsonResponse
from django.urls import reverse
from accounts.models import UserAdditionalInformation

# Create your views here.

class BlogHomeView(View):
    def get(self, request, *args, **kwargs):
        all_category = PostCategory.objects.all().order_by("category")
        all_post = Post.objects.all().order_by("-timestamp")
        #post_url = request.build_absolute_uri(reverse('blog:blog_detail_view', kwargs={'SLUG': post.slug, 'ID': post.id}))
        context = {
            "all_category":all_category,
            "all_post":all_post
        }
        return render(request, "blog/blog_category.html", context)
    

class PostDetailView(View):
    def get(self, request, ID, *args, **kwargs):
        post = get_object_or_404(Post, id=ID)
        all_category = PostCategory.objects.all().order_by("category")
        post_url = request.build_absolute_uri(reverse('blog:blog_detail_view', kwargs={'SLUG': post.slug, 'ID': post.id}))
        share_count = PostShare.objects.filter(post=post).count()
        context = {
            "all_category":all_category,
            "post":post,
            "post_url":post_url,
            "share_count":share_count
        }
        return render(request, "blog/blog_single.html", context)
    

    def post(self, request, ID, *args, **kwargs):
        post_id = int(request.POST.get("post_id"))
        platform = request.POST.get("platform")
        post = get_object_or_404(Post, id=post_id)
        additional_info = UserAdditionalInformation.objects.get(user=request.user)
        if PostShare.objects.filter(id=post_id, user=request.user).exists():
            print("yes")
        else:
            if platform == "fb":
                PostShare.objects.create(user=request.user, post=post, platform_shared="FACEBOOK")
                additional_info.activity_bal = additional_info.activity_bal + 300
                additional_info.save()
            elif platform == "tw":
                PostShare.objects.create(user=request.user, post=post, platform_shared="TWITTER")
                additional_info.activity_bal = additional_info.activity_bal + 300
                additional_info.save()
            elif platform == "li":
                PostShare.objects.create(user=request.user, post=post, platform_shared="LINKEDIN")
                additional_info.activity_bal = additional_info.activity_bal + 300
                additional_info.save()
            elif platform == "wh":
                PostShare.objects.create(user=request.user, post=post, platform_shared="WHATSAPP")
                additional_info.activity_bal = additional_info.activity_bal + 300
                additional_info.save()
                
        return JsonResponse({'message': 'Request successful'})
        