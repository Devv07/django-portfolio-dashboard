from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_content, name='upload_content'),
    path('upload/<str:tab>/', views.upload_content, name='upload_content'),
    path('projects/', views.manage_projects, name='manage_projects'),
    path('blog/', views.manage_blog_posts, name='manage_blog_posts'),
    path('blog/create/', views.create_blog_post, name='create_blog_post'),
    path('blog/edit/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/delete/<int:pk>/', views.delete_blog_post, name='delete_blog_post'),
    path('blog/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('analytics/', views.blog_analytics, name='blog_analytics'),
    path('settings/', views.portfolio_settings, name='portfolio_settings'),
    path('profile/', views.profile_view, name='profile_view'),

     # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]