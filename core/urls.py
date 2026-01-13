from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # تأكد من كتابتها هكذا: admin.site.urls
    path('admin/', admin.site.urls), 
    
    path('', include('debts.urls')),
    
    # مسارات تسجيل الدخول والخروج
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]