from django.contrib import admin

# Register your models here.
from .models import Customer, Jobsite, Ticket

admin.site.register(Customer)
admin.site.register(Jobsite)
admin.site.register(Ticket)