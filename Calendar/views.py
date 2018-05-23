from django.shortcuts import render
from CRM.models import Ticket
from django.views import generic
from django.core import serializers
from CRM.models import Customer, Jobsite, Ticket
from django.views.decorators.cache import never_cache, cache_control

from .models import Appointment
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy

# @login_required(login_url='customers:login')
def CalendarView(request):
    data = ''
    scheduled_appointments = Appointment.objects.filter(unscheduled=False)


    unscheduled = Appointment.objects.all().filter(unscheduled=True).order_by('created')
    open_tickets = Ticket.objects.all().filter(completed=False)
    for appointment in scheduled_appointments:
        data = data + appointment.appt+','
        print(appointment.unscheduled)
        print(data)


    context = {
        "data":data,
        "unscheduled":unscheduled,
        "open_tickets":open_tickets,
    }

    return render(request, "Calendar/calendar.html", context)


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
    success_url = reverse_lazy('calendar')

class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = 'Calendar/appointment_detail.html'
    pk_url_kwarg = 'app'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context