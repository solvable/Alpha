from django.db import models
from CRM.models import Customer, Jobsite, Ticket
from Calendar.choices import TIME_SLOTS, EMPLOYEE
from django.shortcuts import reverse


# Create your models here.
class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    jobsite = models.ForeignKey(Jobsite, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    schedule_date = models.DateField(null=True, blank=True)
    unscheduled = models.BooleanField(default=True)
    time_slot = models.CharField(blank=True, choices=TIME_SLOTS, default='', max_length=20, null=True)
    start = models.CharField(null=True, max_length=30, blank=True)
    end = models.CharField(null=True, max_length=30, blank=True)
    estimator = models.CharField(choices=EMPLOYEE, null=True, max_length=20, default='red')
    title = models.CharField(blank=True, max_length=50)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    appt = models.CharField(null=True, max_length=200, blank=True)


    def get_absolute_url(self):
        return reverse("appointment-detail", kwargs={"app":self.id})


    def save(self):

        self.title = self.ticket.customer_id.fullName
        if self.time_slot == 't0810':
            start = "08:00"
            end = "10:00"
        elif self.time_slot == 't0911':
            start = "09:00"
            end = "11:00"
        elif self.time_slot == 't1012':
            start = "10:00"
            end = "12:00"
        elif self.time_slot == 't1113':
            start = "11:00"
            end = "13:00"
        elif self.time_slot == 't1214':
            start = "12:00"
            end = "14:00"
        elif self.time_slot == 't1315':
            start = "13:00"
            end = "15:00"
        else:
            start = "14:00"
            end = "16:00"
        self.start = start
        self.end = end
        super(Appointment, self).save()
        url = self.get_absolute_url()

        self.appt = str("{title:'" + str(self.title) +"', start:'"+ str(self.schedule_date) +"T"+(self.start) +"', end:'" + str(self.schedule_date)+"T"+str(self.end) +"', color:'" + str(self.estimator) +"', pk:'" +str(self.pk) +"', url:'http://127.0.0.1:8000"+str(url)+"'}")
        if self.schedule_date:
            self.unscheduled = False

        super(Appointment, self).save()

