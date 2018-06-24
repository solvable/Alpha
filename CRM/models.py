from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.
from django.conf import settings
from django.db import models
import geocoder
from django.urls import reverse
from .choices import *
import os
from .api import googlemaps as googlemapsAPI
os.environ["GOOGLE_API_KEY"] = googlemapsAPI
from django.dispatch import receiver
from django.core.signals import request_finished



class Customer(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete="CASCADE")
    modified_by=models.CharField(max_length=50,default=1)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    fullName = models.CharField(max_length=50, blank=True)
    billStreet = models.CharField(max_length=25)
    billCity = models.CharField(max_length=20)
    billState = models.CharField(max_length=2)
    billZip = models.CharField(max_length=5)
    latlng = models.CharField(blank=True, max_length=100, default = '')
    lat = models.FloatField(blank=True,max_length=100, default = '')
    lng = models.FloatField(blank=True, max_length=100, default='')
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=20, default=NOTAPP)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Geocode Full Address
    def save(self, *args, **kwargs):
        full_address = str(self.billStreet + " " + self.billCity + " " + self.billState + " " + self.billZip)
        g = geocoder.google(full_address)
        lat = str(g.json['lat'])
        lng = str(g.json['lng'])
        self.fullName = str(self.firstName+" "+self.lastName)
        self.lat = lat
        self.lng = lng
        self.latlng = lat + "," + lng

        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.fullName)

    def __str__(self):
        return str(self.fullName)

    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"cust": self.pk})

    def edit_url(self):
        return reverse("customer_edit", args={"cust":self.pk})

    class Meta:
        ordering = ["-created", "-modified"]


class Jobsite(models.Model):

    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete="PROTECT")
    modified_by = models.CharField(max_length=50, default=1)
    jobStreet = models.CharField(max_length=25)
    jobCity = models.CharField(max_length=20)
    jobState = models.CharField(max_length=2)
    jobZip = models.CharField(max_length=5)
    stories = models.IntegerField()
    access = models.CharField(max_length=20)
    notes = models.CharField(max_length=150, blank=True)
    picture = models.ImageField(null=True,blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    latlng = models.CharField(blank=True, max_length=100, default="")
    lat = models.FloatField(blank=True, max_length=100, default=0)
    lng = models.FloatField(blank=True, max_length=100, default=0)
    class Meta:
        ordering = ["-created", "-modified"]

    # Geocode Full Address and Save
    def save(self, *args, **kwargs):
        # Geolocate
        full_address = str(self.jobStreet + " " + self.jobCity + " " + self.jobState + " " + self.jobZip)
        g = geocoder.google(full_address)
        lat = str(g.json['lat'])
        lng = str(g.json['lng'])
        self.lat = lat
        self.lng = lng
        self.latlng = lat + "," + lng
        self.slug=slugify(self.jobStreet)
        super(Jobsite, self).save(*args, **kwargs)


    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.jobStreet)

    def __delete__(self, instance):
        return reverse("jobsite_detail", args=[str(self.id)])

    def get_absolute_url(self):
        return reverse("jobsite_detail", kwargs={"job":self.id, "cust":self.customer_id.id})

    def edit_url(self):
        return reverse("jobsite_detail", kwargs={"job":self.id})




class Ticket(models.Model):

    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    jobsite_id = models.ForeignKey('Jobsite', on_delete=models.CASCADE)
    call_type = models.CharField(choices=TITLES, max_length=10)
    problem = models.CharField(max_length=200, null=True)
    completed = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    modified_by = models.CharField(max_length=50, default=1, null=True)
    notes = models.TextField(max_length=200, default='', null=True)
    printed = models.BooleanField(default=False)
    assigned_to = models.CharField(max_length=50, blank=True, default='Unassigned')

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)

    def __unicode(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def __delete__(self, instance):
        return reverse("ticket_detail")

    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"ticket": self.id, "cust": self.customer_id.id, "job": self.jobsite_id_id})




# method for updating

@receiver(request_finished)
def update_ticket(sender, **kwargs):
    print(kwargs)
    appointment = kwargs['instance']
    ticket = Ticket.objects.get(pk = appointment.ticket.id)
    ticket.assigned_to = appointment.estimator_id
    print(ticket.assigned_to)
    ticket.save()
