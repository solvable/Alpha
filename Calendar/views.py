from django.shortcuts import render
from CRM.models import Ticket
from django.views import generic
from django.core import serializers
from CRM.models import Customer, Jobsite, Ticket
from django.views.decorators.cache import never_cache, cache_control

from .models import Appointment
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404, redirect, reverse, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import json

# @login_required(login_url='customers:login')

@ensure_csrf_cookie
def CalendarView(request):
    data_list =  []
    data = ''
    open_tickets = Ticket.objects.all().filter(completed=False)
    unscheduled = Appointment.objects.all().filter(unscheduled=True).order_by('created')

    # scheduled_appointments = Appointment.objects.filter(unscheduled=False)
    # for appointment in scheduled_appointments:
    #     data = data + appointment.appt+','
    #     print(appointment.unscheduled)
    #     print(data)


    data_list =  Appointment.objects.all().values_list('appt', flat=True)

    print(data_list)


    data = ",".join(data_list)

    print(data)


    context = {
        "data":data,
        "unscheduled":unscheduled,
        "open_tickets":open_tickets,
    }

    return render(request, "Calendar/calendar.html", context)


def save_event(request):
    appointment_pk = request.POST.get('pk')
    date = request.POST.get('start')
    date = date[:10]
    print(date)
    print('Appointment:'+ appointment_pk)
    appointment = Appointment.objects.get(id=appointment_pk)
    print(appointment)
    appointment.title = request.POST.get('title')
    appointment.schedule_date = date
    appointment.start = request.POST.get('start')
    appointment.end = request.POST.get('end')
    print(appointment.start + appointment.end)
    appointment.color = request.POST.get('color')
    appointment.url = request.POST.get('url')
    try:
        appointment.save()
        print('saved:' + appointment_pk)
        print('New Date: '+appointment.schedule_date+ 'New Time:'+ appointment.start +'-'+appointment.end)
    except:
        print('error')
    # Return a response. An empty dictionary is still a 200
    return HttpResponse(json.dumps([{}]), content_type='application/json')


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'Calendar/appointment_form.html'

    # def save(self):
    #     self.title = self.ticket.customer_id.fullName
    #     if self.time_slot == 't0810':
    #         start = "08:00"
    #         end = "10:00"
    #     elif self.time_slot == 't0911':
    #         start = "09:00"
    #         end = "11:00"
    #     elif self.time_slot == 't1012':
    #         start = "10:00"
    #         end = "12:00"
    #     elif self.time_slot == 't1113':
    #         start = "11:00"
    #         end = "13:00"
    #     elif self.time_slot == 't1214':
    #         start = "12:00"
    #         end = "14:00"
    #     elif self.time_slot == 't1315':
    #         start = "13:00"
    #         end = "15:00"
    #     else:
    #         start = "14:00"
    #         end = "16:00"
    #     self.start = start
    #     self.end = end
    #     super(Appointment, self).save()
    #
    #     self.appt = str("{title:'" + str(self.title) +"', start:'"+ "T"+(self.start) +"', end:'" + "T"+str(self.end) +"', color:'" + str(self.estimator) +"', pk:'" +str(self.pk) +"', url:'http://127.0.0.1:8000"+str(url)+"'}")
    #
    #     super(Appointment, self).save()

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

    # def save(self):
    #     super(Appointment, self).save()
    #     self.title = self.ticket.customer_id.fullName
    #     if self.time_slot == 't0810':
    #         start = "08:00"
    #         end = "10:00"
    #     elif self.time_slot == 't0911':
    #         start = "09:00"
    #         end = "11:00"
    #     elif self.time_slot == 't1012':
    #         start = "10:00"
    #         end = "12:00"
    #     elif self.time_slot == 't1113':
    #         start = "11:00"
    #         end = "13:00"
    #     elif self.time_slot == 't1214':
    #         start = "12:00"
    #         end = "14:00"
    #     elif self.time_slot == 't1315':
    #         start = "13:00"
    #         end = "15:00"
    #     else:
    #         start = "14:00"
    #         end = "16:00"
    #     self.start = start
    #     self.end = end
    #     super(Appointment, self).save()
    #     self.appt = str("{title:'" + str(self.title) +"', start:'"+ str(self.schedule_date) +"T"+(self.start) +"', end:'" + str(self.schedule_date)+"T"+str(self.end) +"', color:'" + str(self.estimator) +"', pk:'" +str(self.pk) +"', url:'http://127.0.0.1:8000"+str(url)+"'}")
    #
    #     super(Appointment, self).save()

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