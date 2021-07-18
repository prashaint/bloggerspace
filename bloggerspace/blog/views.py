from django.db.models.base import Model
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Post, Author, Tag
from django.views.generic import ListView, UpdateView, DeleteView
from django.views import View
from .forms import Comment, CommentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import PostForm

# Create your views here.

class UserPostView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

class PostDetailView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id") 
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail", args=[slug]))
            
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id") 
        }
        return render(request, "blog/post-detail.html", context)

def new_blog_post(request):
	if request.method == 'GET':
		return render(request, 'blog/new_blog_post.html', {'form':PostForm()})
	else:
		if request.method == 'POST':
			new_blog = Post()
			new_post_form = PostForm(request.POST, instance=new_blog)
			new_post = new_post_form.save()
			return redirect('blog:curr_user_blogs')
		else:
			return render(request, 'blog/new_blog_post.html', {'form':PostForm()})

class UpdatePostView(UpdateView):
	model = Post
	template_name = 'blog/update_post.html'
	fields = [ 'title', 'excerpt', 'image', 'content', 'tags' ]
		
	def get_success_url(self):
		return reverse('blog:curr_user_blogs')

class DeletePostView(DeleteView):
	model = Post
	template_name = 'blog/delete_post.html'

	def get_success_url(self):
		return reverse('blog:curr_user_blogs')       


def user_signup(request):
	if request.method == 'GET': 
		return render(request, 'blog/user_signup.html', {'form':UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('blog:curr_user_blogs')
			except IntegrityError:
				return render(request, 'blog/user_signup.html', {'form':UserCreationForm(), 'error':'Username already exists. Please choose another name.'})
		else:
			return render(request, 'blog/user_signup.html', {'form':UserCreationForm(), 'error':'Password and Confirmation Password did not match.'})

def user_login(request):
	if request.method == 'GET': 
		return render(request, 'blog/user_login.html', {'form':AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'blog/user_login.html', {'form':AuthenticationForm(), 'error':'Username or Password did not match'})
		else:
			login(request, user)
			return redirect('blog:curr_user_blogs')

def user_logout(request):
	if request.method == 'POST':
		logout(request)
		return render(request, 'blog/user_logout.html')

def curr_user_blogs(request):
	blogs = Post.objects.all()
	return render(request, 'blog/index.html')


