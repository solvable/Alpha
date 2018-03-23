from django.views import generic
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404



# Create your views here.


from .models import Customer, Jobsite, Ticket


class IndexView(generic.ListView):
    model = Customer
    template_name = 'CRM/index.html'


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
