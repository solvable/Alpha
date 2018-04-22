from django.forms.models import inlineformset_factory
from .models import Estimate, Section

EstimateFormSet = inlineformset_factory(Estimate, Section, fields=('__all__'))