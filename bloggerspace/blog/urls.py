from django.urls import path
from . import views
from .views import UpdatePostView, DeletePostView

app_name = 'blog'

urlpatterns = [
    path("", views.UserPostView.as_view(), name="start_page"),
    path("posts", views.AllPostsView.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail"),
    path('user_signup/', views.user_signup, name="user_signup"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('new_blog_post/', views.new_blog_post, name="new_blog_post"),
    path('user_posts/', views.UserPostView.as_view(), name="user_posts"),
    path('user_posts/<slug:slug>', views.UpdatePostView.as_view(), name='update_blog_post'),
    path('user_posts/<slug:slug>/DeletePost', views.DeletePostView.as_view(), name='delete_post'),
]

