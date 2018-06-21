from django.contrib import admin

# Register your models here.
from CRM.models import Customer, Jobsite, Ticket
from Estimates.models import Estimate, Section
from Calendar.models import Appointment
from Profile.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)







admin.site.register(Customer)
admin.site.register(Jobsite)
admin.site.register(Ticket)
admin.site.register(Estimate)
admin.site.register(Section)
admin.site.register(Appointment)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)