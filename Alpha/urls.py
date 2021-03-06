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
from django.conf.urls import include, url
from django.conf import settings
from CRM import views
from Estimates.views import EstimateCreateView, EstimateDetailView, EstimateUpdateView, EstimateDeleteView, write_pdf_view, write_docx_view, write_invoice_view, convertEstimateToJob
from Calendar.views import CalendarView, AppointmentCreateView, AppointmentUpdateView, AppointmentDeleteView, AppointmentDetailView, save_event
from Map.views import MapView
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views
import django.contrib.auth.urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.LandingView, name='index'),

    path('index/', views.IndexView, name='index'),

    path('customer/<cust>/detail/<job>/ticket_create', views.TicketCreateView.as_view(), name='ticket_create'),
    path('customer/<cust>/detail/<job>/detail/<ticket>', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('customer/<cust>/detail/<job>/update/<ticket>', views.TicketUpdateView.as_view(), name='ticket_update'),
    path('customer/<cust>/detail/<job>/delete/<ticket>', views.TicketDeleteView.as_view(), name='ticket_delete'),

    path('customer/<cust>/detail/jobsite_create/', views.JobsiteCreateView.as_view(), name='jobsite_create'),
    path('customer/<cust>/detail/<job>', views.JobsiteDetailView.as_view(), name='jobsite_detail'),
    path('customer/<cust>/update/<job>', views.JobsiteUpdateView.as_view(), name='jobsite_update'),
    path('customer/<cust>/delete/<job>', views.JobsiteDeleteView.as_view(), name ='jobsite_delete'),

    path('customer/detail/<cust>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/update/<cust>', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/delete/<cust>', views.CustomerDeleteView.as_view(), name='customer_delete'),

    path('customer/<cust>/detail/<job>/<ticket>/detail/generate-pdf', write_pdf_view, name='generate-pdf'),
    path('customer/<cust>/detail/<job>/<ticket>/detail/<est>/generate-docx', write_docx_view, name='generate-docx'),
    path('customer/<cust>/detail/<job>/<ticket>/detail/<est>/generate-invoice', write_invoice_view, name='generate-invoice'),
    path('create-estimate/<cust>/<job>/<ticket>', EstimateCreateView.as_view(), name='estimate-create'),
    path('customer/<cust>/detail/<job>/<ticket>/detail/<est>', EstimateDetailView.as_view(), name='estimate-detail'),
    path('customer/<cust>/detail/<job>/<ticket>/update/<est>', EstimateUpdateView.as_view(), name='estimate-update'),
    path('customer/<cust>/detail/<job>/<ticket>/delete/<est>', EstimateDeleteView.as_view(), name='estimate-delete'),
    path('customer/<cust>/detail/<job>/<ticket>/convert/<est>', convertEstimateToJob, name='convert-estimate'),
    path('calendar/', CalendarView, name='calendar'),
    # path('calendar/', CalendarView.as_view(), name='calendar'),
    path('appointment-create/<cust>/<job>/<ticket>', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointment-edit/<app>', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointment-detail/<app>', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointment-delete/<app>', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('save_event', save_event, name='save_event'),

    path('map/', MapView, name='map')

              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^search/', include('haystack.urls')),

                  ] + urlpatterns

