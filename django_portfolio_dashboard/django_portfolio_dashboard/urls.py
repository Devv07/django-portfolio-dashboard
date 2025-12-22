from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

def root_redirect(request):
    return redirect('login')   # name of login url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),   # 👈 this fixes 404
    path('dashbaord/', include('django.contrib.auth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard:login'), name='logout'),
]


# For media files in development (optional but useful)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)