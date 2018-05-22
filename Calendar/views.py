from django.shortcuts import render
from CRM.models import Ticket
from django.views import generic
from django.core import serializers
from CRM.models import Customer, Jobsite, Ticket

from .models import Appointment
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404, redirect, reverse



class CalendarView(generic.ListView):
    model = Appointment
    template_name = 'Calendar/calendar.html'

    scheduled_appointments = Appointment.objects.filter(unscheduled=False)
    # data = serializers.serialize('json', scheduled_appointments, fields=('appt'))

    data = ''
    for appointment in scheduled_appointments:
        data = data + appointment.appt +","
        print(appointment.unscheduled)
        print(data)




    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.data
        return context




class AppointmentCreateView(generic.CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'Calendar/appointment_form.html'



    def get_success_url(self):
        return reverse('calendar')

    def get_initial(self):
        customer = get_object_or_404(Customer, id=self.kwargs.get('cust'))
        jobsite = get_object_or_404(Jobsite, id=self.kwargs.get('job'))
        ticket =  get_object_or_404(Ticket, id=self.kwargs.get('ticket'))

        return{
            'customer':customer.id,
            'jobsite':jobsite.id,
            'ticket':ticket.id,
        }




    def form_valid(self, form):
        context = self.get_context_data()


        if form.is_valid():
            self.object = form.save(commit=False)
            form.save()

        return redirect(self.get_success_url())



class AppointmentUpdateView(generic.UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'Calendar/appointment_form.html'
    pk_url_kwarg = 'app'


class AppointmentDeleteView(generic.DeleteView):
    model = Appointment
    pk_url_kwarg = 'app'


class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = 'Calendar/appointment_detail.html'
    pk_url_kwarg = 'app'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context