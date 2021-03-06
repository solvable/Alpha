from django.db import models
from tinymce.models import HTMLField
from django.conf import settings
from CRM.models import Customer, Jobsite, Ticket
from django.urls import reverse
from datetime import date
from datetime import timedelta
from Estimates.choices import GUARANTEE_CHOICES
# Create your models here.


class Estimate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete="PROTECT")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    jobsite = models.ForeignKey(Jobsite, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete="CASCADE")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    name = models.CharField(max_length=100)
    billStreet = models.CharField(max_length=100)
    billCityStateZip = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    job_address= models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    completedDate = models.DateField(null=True, blank=True)
    paid = models.BooleanField(blank=True, default=False)
    scheduleDate = models.DateField(blank=True, null=True)
    sold  = models.BooleanField(default=False)


    # Geocode Full Address
    def save(self, *args, **kwargs):
        super(Estimate, self).save(*args, **kwargs)

        dollar = 0
        for i in self.section_set.all():
            dollar = dollar + i.price

        self.total = dollar

        if self.completed:
            self.completedDate = date.today() - timedelta(1)



        super(Estimate, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("estimate_detail", kwargs={"cust":self.customer_id, "job":self.jobsite_id, "ticket":self.ticket_id, "est": self.pk})
    #
    # def edit_url(self):
    #     return reverse("estimate_edit", args={"est":self.pk})

    class Meta:
        ordering = ["-created", "-modified"]




class Section(models.Model):
    heading = models.CharField(max_length=100, null=False)
    description = models.TextField()
    guarantee = models.CharField(max_length=2, blank=True, choices=GUARANTEE_CHOICES, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, default='')


    def save(self, *args, **kwargs):
        super(Section, self).save(*args, **kwargs)



    def __unicode__(self):
        return str(self.heading)


    def __str__(self):
        return str(self.heading)

    #
    # def get_absolute_url(self):
    #     return reverse("section", kwargs={"est": self.pk})
    #

    #
    # def edit_url(self):
    #     return reverse("estimate_edit", args={"est":self.pk})

    class Meta:
        managed = True
