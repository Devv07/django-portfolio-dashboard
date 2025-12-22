from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_content, name='upload_content'),
    path('projects/', views.manage_projects, name='manage_projects'),
    path('blog/', views.manage_blog, name='manage_blog'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings, name='settings'),
]