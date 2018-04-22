from django.shortcuts import render
from django.views import generic
from .models import Estimate, Section
from CRM.models import Customer, Jobsite, Ticket
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.views.generic.edit import FormMixin
from django.views import generic
from .forms import EstimateFormSet


class CreateEstimateView(generic.CreateView):
    model = Estimate
    template_name = 'estimate/create_estimate.html'
    fields = ['name', 'billStreet', 'billCityStateZip', 'phone', 'email', 'job_address', 'total']


    def get_initial(self):
        customer = get_object_or_404(Customer, id=self.kwargs.get('cust'))
        jobsite = get_object_or_404(Jobsite, id=self.kwargs.get('job'))
        ticket =  get_object_or_404(Ticket, id=self.kwargs.get('ticket'))


    def get_context_data(self, **kwargs):
        context = super(CreateEstimateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['section_formset'] = EstimateFormSet(self.request.POST)
        else:
            context['section_formset'] = EstimateFormSet()
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['section_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return {
            'name': customer.fullName,
            'billStreet': customer.billStreet,
            'billCityStateZip': "%s, %s, %s" % (customer.billCity, customer.billState, customer.billZip),
            'job_address': jobsite.jobStreet,
            'phone': customer.phone1,
            'email':customer.email,


        }

