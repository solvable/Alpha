from django.forms import ModelForm
from django.forms.widgets import DateInput
from Calendar.models import Appointment


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        # fields = ['schedule_date','time_slot','color','notes']
        fields = '__all__'
        widgets = {
            'schedule_date': DateInput(attrs={'class':'datepicker'}),
        }
