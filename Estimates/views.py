from django.shortcuts import render
from django.views import generic
from .models import Estimate, Section
from CRM.models import Customer, Jobsite, Ticket
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.views.generic.edit import FormMixin
from django.views import generic
from django.shortcuts import redirect
from .forms import SectionFormset, EstimateForm, SectionInline, SectionForm
from django.urls import reverse

class EstimateCreateView(generic.CreateView):
    model = Estimate
    template_name = 'estimate/create_estimate.html'
    fields = ['customer', 'jobsite', 'ticket', 'name', 'billStreet', 'billCityStateZip', 'phone', 'email', 'job_address']

    def get_success_url(self):
        return reverse('estimate-detail', kwargs={'cust': self.object.customer, 'job': self.object.jobsite, 'ticket': self.object.ticket, 'est': self.object.id})

    def get_initial(self):
        customer = get_object_or_404(Customer, id=self.kwargs.get('cust'))
        jobsite = get_object_or_404(Jobsite, id=self.kwargs.get('job'))
        ticket =  get_object_or_404(Ticket, id=self.kwargs.get('ticket'))

        return{
            'customer':customer.id,
            'jobsite':jobsite.id,
            'ticket':ticket.id,
            'name': customer.fullName,
            'billStreet': customer.billStreet,
            'billCityStateZip': "%s, %s, %s" % (customer.billCity, customer.billState, customer.billZip),
            'job_address': jobsite.jobStreet,
            'phone': customer.phone1,
            'email':customer.email,
        }

    def get_context_data(self, **kwargs):
        context = super(EstimateCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['sectionform'] = SectionFormset(self.request.POST, prefix='section')
        else:
            context['sectionform'] = SectionFormset(prefix='section')
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        section_form = context['sectionform']

        if form.is_valid() and section_form.is_valid():
            self.object = form.save(commit=False)
            section_form.instance = self.object
            section_form.save(commit=False)
            form.save()
            section_form.save()
            form.save()




            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EstimateUpdateView(generic.UpdateView):
    model = Estimate
    template_name = 'estimate/create_estimate.html'
    pk_url_kwarg = 'est'
    fields='__all__'

    def get_success_url(self):
        return reverse('estimate-detail', kwargs={'cust': self.object.customer, 'job': self.object.jobsite, 'ticket': self.object.ticket, 'est': self.object.id})


    def get_context_data(self, **kwargs):
        context = super(EstimateUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['sectionform'] = SectionFormset(self.request.POST, instance=self.object, prefix='section')

        else:
            context['sectionform'] = SectionFormset(instance=self.object, prefix='section')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        section_form = context['sectionform']

        if form.is_valid() and section_form.is_valid():
            self.object = form.save(commit=False)
            section_form.instance = self.object
            section_form.save(commit=False)
            section_form.save()
            form.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))







class EstimateDetailView(generic.DetailView):
    model=Estimate
    template_name = 'estimate/estimate_detail.html'
    pk_url_kwarg = "est"



class EstimateDeleteView(generic.DeleteView):
    model = Estimate
    template_name = 'estimate/estimate_confirm_delete.html'
    pk_url_kwarg = "est"

    def get_success_url(self):
        return reverse('ticket_detail', kwargs={'cust': self.kwargs.get('cust'), 'job': self.kwargs.get('job'), 'ticket': self.kwargs.get('ticket')})
