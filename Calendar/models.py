from django.db import models
from CRM.models import Customer, Jobsite, Ticket
from Calendar.choices import EMPLOYEE
from django.shortcuts import reverse


# Create your models here.
class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    jobsite = models.ForeignKey(Jobsite, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    schedule_date = models.DateField(null=True, blank=True)
    unscheduled = models.BooleanField(default=True)
    # time_slot = models.CharField(blank=True, choices=TIME_SLOTS, default='', max_length=20, null=True)
    start = models.CharField(null=True, max_length=30, blank=True)
    end = models.CharField(null=True, max_length=30, blank=True)
    estimator = models.CharField(choices=EMPLOYEE, null=True, max_length=20, default='red')
    title = models.CharField(blank=True, max_length=50)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    appt = models.CharField(null=True, max_length=250, blank=True)


    def get_absolute_url(self):
        return reverse("appointment-detail", kwargs={"app":self.id})


    def save(self):

        self.title = self.ticket.customer_id.fullName

        self.date = self.schedule_date
        super(Appointment, self).save()
        url = self.get_absolute_url()
        self.appt=''
        super(Appointment, self).save()
        self.appt = str("{title:'" + str(self.title) +"', date:'"+ str(self.schedule_date) +"', start:'"+str(self.schedule_date) +(self.start) +"', end:'" + str(self.schedule_date)+str(self.end) +"', color:'" + str(self.estimator)+"', startEditable:'" + 'True' +"', pk:'" +str(self.pk) +"', url:'http://127.0.0.1:8000"+str(url)+"'}")
        if self.schedule_date:
            self.unscheduled = False
        if self.estimator:
            self.ticket.assigned_to = self.estimator

        super(Appointment, self).save()

