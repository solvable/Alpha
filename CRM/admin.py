from django.contrib import admin

# Register your models here.
from CRM.models import Customer, Jobsite, Ticket
from Estimates.models import Estimate, Section
from Calendar.models import Appointment


admin.site.register(Customer)
admin.site.register(Jobsite)
admin.site.register(Ticket)
admin.site.register(Estimate)
admin.site.register(Section)
admin.site.register(Appointment)