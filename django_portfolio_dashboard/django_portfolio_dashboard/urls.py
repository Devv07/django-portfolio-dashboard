# your_project/urls.py (main project urls.py)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public Portfolio - accessible to everyone
    path('', include('portfolio.urls')),

    # Private Dashboard
    path('dashboard/', include('dashboard.urls')),

    # Dashboard Login Page
    path('dashboard/login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html'  # your custom login template
    ), name='dashboard_login'),

    # Dashboard Logout - FIXED: explicit redirect to your login page
    path('dashboard/logout/', auth_views.LogoutView.as_view(
        next_page='/dashboard/login/'  # ← This fixes the error
    ), name='dashboard_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)