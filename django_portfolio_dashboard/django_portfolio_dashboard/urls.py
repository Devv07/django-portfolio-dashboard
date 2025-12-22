from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    return redirect('login')   # name of login url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),   # 👈 this fixes 404
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', include('dashboard.urls')),
]
