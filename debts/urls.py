from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]