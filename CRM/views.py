import datetime
import os
from io import BytesIO
from django.utils import timezone
from django.db.models.signals import post_save

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.shortcuts import render

from Estimates.models import Estimate, Section
from Calendar.models import Appointment
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Customer, Jobsite, Ticket


def LandingView(request):

    login_message = "Please Login to continue"

    context = {
        "login_message":login_message,
    }

    return render(request, 'CRM/landing.html',context)





@login_required
def IndexView(request):
        now = timezone.now()
        open_tickets = Ticket.objects.filter(completed=False)[:]
        latest_tickets = Ticket.objects.order_by('-created')[:5]
        service_call_total = Ticket.objects.filter(call_type='Service').filter(created__year=now.year).count()

        tickets_ytd = Ticket.objects.filter(created__year=now.year).count()
        jobs_complete_ytd = Estimate.objects.count()
        chalie_tickets = open_tickets.filter(assigned_to='Chalie').count()
        evan_tickets = open_tickets.filter(assigned_to='Evan').count()
        barry_tickets = open_tickets.filter(assigned_to='Barry').count()
        timmy_tickets = open_tickets.filter(assigned_to='Timmy').count()

        if tickets_ytd:
            service_percent = round((service_call_total/ tickets_ytd)*100,0)
        else:
            service_percent = "N/A"

        unpaid_invoices = Estimate.objects.filter(completed=True, paid=False)
        street = 0
        if unpaid_invoices:
            for i in unpaid_invoices:
                street = street + i.total
            else:
                street = 0

        unscheduled_jobs = Estimate.objects.filter(completed=False, sold=True)

        old_tickets = open_tickets.filter(created=datetime.now()-timedelta(days=14))

        context = {
        "latest_tickets": latest_tickets,
        "open_tickets": open_tickets,
        "unpaid_invoices": unpaid_invoices,
        "street_balance": street,
        "tickets_ytd": tickets_ytd,
        "jobs_complete_ytd": jobs_complete_ytd,
        "open_ticket_count": open_tickets.count(),
        "chalie_tickets": chalie_tickets,
        "barry_tickets": barry_tickets,
        "evan_tickets": evan_tickets,
        "timmy_tickets": timmy_tickets,
        "service_call_YTD": service_call_total,
        "service_percent": service_percent,
        "unscheduled_jobs": unscheduled_jobs,
        "old_tickets":old_tickets,

    }


        return render(request, "CRM/index.html", context)









'''
Customer Views
'''


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    template_name = 'CRM/customer_detail.html'
    pk_url_kwarg = "cust"


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    template_name = 'CRM/customer_create.html'
    pk_url_kwarg = "cust"
    fields = ['firstName', 'lastName', 'billStreet', 'billCity', 'billState', 'billZip', 'phone1', 'phone2', 'email',
              'source']


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    template_name = 'CRM/customer_update.html'
    pk_url_kwarg = "cust"
    fields = ['firstName', 'lastName', 'billStreet', 'billCity', 'billState', 'billZip', 'phone1', 'phone2', 'email',
              'source']

class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    pk_url_kwarg = 'cust'
    success_url = reverse_lazy('index')


'''
Jobsite Views
'''

class JobsiteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Jobsite
    template_name = 'CRM/jobsite_detail.html'
    pk_url_kwarg = "job"




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.kwargs['cust'])
        return context

class JobsiteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Jobsite
    template_name = 'CRM/jobsite_create.html'
    pk_url_kwarg = "cust"
    fields = ['customer_id', 'jobStreet', 'jobCity', 'jobState', 'jobZip', 'stories', 'access', 'notes']

    def get_initial(self):
        customer = get_object_or_404(Customer, pk=self.kwargs.get('cust'))
        return {
            'customer_id': customer.id,
        }

class JobsiteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Jobsite
    template_name = 'CRM/jobsite_create.html'
    fields = ['customer_id', 'jobStreet', 'jobCity', 'jobState', 'jobZip', 'stories', 'access', 'notes']

    pk_url_kwarg = "job"

class JobsiteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Jobsite
    pk_url_kwarg = "job"

    # template_name = 'CRM/jobsite_delete.html'
    def get_success_url(self):
        return reverse('customer_detail', kwargs={'cust': self.kwargs.get('cust')})


'''
Ticket Views
'''

class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ticket
    template_name = 'CRM/ticket_detail.html'
    pk_url_kwarg = "ticket"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.kwargs['cust'])
        context['jobsite'] = get_object_or_404(Jobsite, id=self.kwargs['job'])
        # context['appt'] = get_object_or_404(Appointment, id=self.kwargs['appt'])
        return context


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    template_name = 'CRM/ticket_create.html'
    pk_url_kwarg = "job"
    fields = ['customer_id', 'jobsite_id', 'call_type', 'problem', 'completed', 'notes']

    def get_initial(self):
        customer = get_object_or_404(Customer, id=self.kwargs.get('cust'))
        jobsite = get_object_or_404(Jobsite, id=self.kwargs.get('job'))

        return {
            'customer_id': customer.id,
            'jobsite_id': jobsite.id
        }


class TicketUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ticket
    template_name = 'CRM/ticket_create.html'
    fields = ['customer_id', 'jobsite_id', 'call_type', 'problem', 'completed', 'notes']
    pk_url_kwarg = "ticket"

class TicketDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ticket
    pk_url_kwarg = "ticket"

    def get_success_url(self):
        return reverse('jobsite_detail', kwargs={'cust': self.kwargs.get('cust'), 'job': self.kwargs.get('job')})
