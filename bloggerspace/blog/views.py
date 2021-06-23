from django.shortcuts import render, get_list_or_404
from .models import Post, Author, Tag

# Create your views here.

def start_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })

def post_detail(request, slug):
    #found_post=get_list_or_404(Post, slug=slug)
    found_post = Post.objects.get(slug=slug)
    return render(request, "blog/post-detail.html", {
        "post": found_post,
        
    })
