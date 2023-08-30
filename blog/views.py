from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PostCategory, Post
from django.http import HttpResponse
from django.urls import reverse

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
        context = {
            "all_category":all_category,
            "post":post,
            "post_url":post_url
        }
        return render(request, "blog/blog_single.html", context)
    