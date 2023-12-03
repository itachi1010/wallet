# blog/urls.py
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView, UserPostListView,
)
from . import views


urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='blog-index'),
    path('home/', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),  # add path
    path('about/', views.about, name='blog-about'),

]
