"""Alpha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CRM import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', views.IndexView.as_view(), name='index'),
    path('customer/detail/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/update/<int:pk>', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/delete/<int:pk>', views.CustomerDeleteView.as_view(), name ='customer_delete'),
    path('customer/detail/<int:pk>/<slug>', views.JobsiteDetailView.as_view(), name='jobsite_detail'),
    path('customer/detail/<int:pk>/jobsite_create/', views.JobsiteCreateView.as_view(), name='jobsite_create'),

]
