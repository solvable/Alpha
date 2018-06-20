import datetime
import os
from io import BytesIO
from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from Estimates.models import Estimate, Section
from Calendar.models import Appointment
from django.views.decorators.cache import never_cache, cache_control


from .models import Customer, Jobsite, Ticket
from django.utils.decorators import method_decorator

class IndexView(generic.ListView):
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        return super(IndexView,self).dispatch(request,*args,**kwargs)
    now = timezone.now()



    model = Ticket
    template_name = 'CRM/index.html'
    open_tickets = Ticket.objects.filter(completed=False)[:]
    latest_tickets = Ticket.objects.order_by('-created')[:5]
    service_call_total = Ticket.objects.filter(call_type='Service').filter(created__year=now.year).count()

    tickets_ytd = Ticket.objects.filter(created__year=now.year).count()
    jobs_complete_ytd = Estimate.objects.count()
    chalie_tickets = open_tickets.filter(assigned_to='Chalie').count()
    evan_tickets = open_tickets.filter(assigned_to='Chalie').count()
    barry_tickets = open_tickets.filter(assigned_to='Chalie').count()
    timmy_tickets = open_tickets.filter(assigned_to='Chalie').count()
    service_percent = round((service_call_total/ tickets_ytd)*100,0)





    unpaid_invoices = Estimate.objects.filter(completed=True, paid=False)
    street = 0
    if unpaid_invoices:
        for i in unpaid_invoices:
            street = street + i.total
    else:
        street = 0


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_tickets'] = IndexView.latest_tickets
        context['open_tickets'] = IndexView.open_tickets
        context['unpaid_invoices'] = IndexView.unpaid_invoices
        context['street_balance'] = IndexView.street
        context['tickets_ytd'] = IndexView.tickets_ytd
        context['jobs_complete_ytd'] = IndexView.jobs_complete_ytd
        context['open_ticket_count'] = IndexView.open_tickets.count()
        context['chalie_tickets'] = IndexView.chalie_tickets
        context['barry_tickets'] = IndexView.barry_tickets
        context['evan_tickets'] = IndexView.evan_tickets
        context['timmy_tickets'] = IndexView.timmy_tickets
        context['service_call_YTD'] = IndexView.service_call_total
        context['service_percent'] = IndexView.service_percent
        return context


'''
Customer Views
'''


class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'CRM/customer_detail.html'
    pk_url_kwarg = "cust"


class CustomerCreateView(generic.CreateView):
    model = Customer
    template_name = 'CRM/customer_create.html'
    pk_url_kwarg = "cust"
    fields = ['firstName', 'lastName', 'billStreet', 'billCity', 'billState', 'billZip', 'phone1', 'phone2', 'email',
              'source']


class CustomerUpdateView(generic.UpdateView):
    model = Customer
    template_name = 'CRM/customer_update.html'
    pk_url_kwarg = "cust"
    fields = ['firstName', 'lastName', 'billStreet', 'billCity', 'billState', 'billZip', 'phone1', 'phone2', 'email',
              'source']


class CustomerDeleteView(generic.DeleteView):
    model = Customer
    pk_url_kwarg = 'cust'
    success_url = reverse_lazy('index')


'''
Jobsite Views
'''


class JobsiteDetailView(generic.DetailView):
    model = Jobsite
    template_name = 'CRM/jobsite_detail.html'
    pk_url_kwarg = "job"




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.kwargs['cust'])
        return context


class JobsiteCreateView(generic.CreateView):
    model = Jobsite
    template_name = 'CRM/jobsite_create.html'
    pk_url_kwarg = "cust"
    fields = ['customer_id', 'jobStreet', 'jobCity', 'jobState', 'jobZip', 'stories', 'access', 'notes']

    def get_initial(self):
        customer = get_object_or_404(Customer, pk=self.kwargs.get('cust'))
        return {
            'customer_id': customer.id,
        }


class JobsiteUpdateView(generic.UpdateView):
    model = Jobsite
    template_name = 'CRM/jobsite_create.html'
    fields = ['customer_id', 'jobStreet', 'jobCity', 'jobState', 'jobZip', 'stories', 'access', 'notes']

    pk_url_kwarg = "job"


class JobsiteDeleteView(generic.DeleteView):
    model = Jobsite
    pk_url_kwarg = "job"

    # template_name = 'CRM/jobsite_delete.html'
    def get_success_url(self):
        return reverse('customer_detail', kwargs={'cust': self.kwargs.get('cust')})


'''
Ticket Views
'''


class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'CRM/ticket_detail.html'
    pk_url_kwarg = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.kwargs['cust'])
        context['jobsite'] = get_object_or_404(Jobsite, id=self.kwargs['job'])
        # context['appt'] = get_object_or_404(Appointment, id=self.kwargs['appt'])
        return context


class TicketCreateView(generic.CreateView):
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


class TicketUpdateView(generic.UpdateView):
    model = Ticket
    template_name = 'CRM/ticket_create.html'
    fields = ['customer_id', 'jobsite_id', 'call_type', 'problem', 'completed', 'notes']
    pk_url_kwarg = "ticket"


class TicketDeleteView(generic.DeleteView):
    model = Ticket
    pk_url_kwarg = "ticket"

    def get_success_url(self):
        return reverse('jobsite_detail', kwargs={'cust': self.kwargs.get('cust'), 'job': self.kwargs.get('job')})
