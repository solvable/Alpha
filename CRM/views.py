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


class CustomerCreateView(generic.CreateView):
    model = Customer
    template_name = 'CRM/customer_create.html'
    fields = ['firstName', 'lastName', 'billStreet', 'billCity', 'billState', 'billZip', 'phone1', 'phone2', 'email', 'source']

class CustomerUpdateView(generic.UpdateView):
    model=Customer
    template_name = 'CRM/customer_update.html'
    fields = ['firstName', 'lastName', 'billStreet', 'billCity', 'billState', 'billZip', 'phone1', 'phone2', 'email', 'source']


class CustomerDeleteView(generic.DeleteView):
    model=Customer
    #template_name = 'CRM/customer_delete.html'
    success_url = reverse_lazy('index')

'''
Jobsite Views
'''


class JobsiteDetailView(generic.DetailView):
    model = Jobsite
    template_name = 'CRM/jobsite_detail.html'
    slug_url_kwarg = "slug"

    customer_model = Customer
    context_object_name = customer_model
    


class JobsiteCreateView(generic.CreateView):
    model = Jobsite
    template_name= 'CRM/jobsite_create.html'
    fields = ['customer_id','jobStreet', 'jobCity', 'jobState', 'jobZip', 'stories', 'access', 'notes']


    def get_success_url(self):
        return reverse('jobsite_detail', kwargs={'cust': self.kwargs.get('customer_id'),
                                                 'slug': self.kwargs.get("slug")})

    def get_initial(self):
        customer = get_object_or_404(Customer, pk=self.kwargs.get('cust'))
        return{
            'customer_id': customer.id,
        }




class JobsiteUpdateView(generic.UpdateView):
    model = Jobsite
    template_name= 'CRM/jobsite_create.html'
    fields = ['customer_id','jobStreet', 'jobCity', 'jobState', 'jobZip', 'stories', 'access', 'notes']


    def get_success_url(self):

        return reverse('jobsite_detail', kwargs={'cust': self.kwargs.get('customer_id'),
                                                 'slug': self.kwargs.get("slug")})





