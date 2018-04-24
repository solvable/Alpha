from django import forms
from .models import Estimate, Section
from django.forms import BaseInlineFormSet, ModelForm, inlineformset_factory


class SectionInline(BaseInlineFormSet):
    model = Section
    fields = '__all__'
    extra = 1

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = '__all__'


SectionFormset = inlineformset_factory(Estimate, Section, fields=('__all__'),  formset=SectionInline,fk_name='estimate')



