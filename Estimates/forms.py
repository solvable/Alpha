from django import forms
from .models import Estimate, Section
from django.forms import BaseInlineFormSet, ModelForm, inlineformset_factory
# from tinymce.widgets import TinyMCE


class SectionInline(BaseInlineFormSet):
    model = Section
    fields = '__all__'


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = '__all__'


SectionFormset = inlineformset_factory(Estimate, Section, fields=('__all__'),  formset=SectionInline,fk_name='estimate', extra=1)
# , widgets={'description': TinyMCE(attrs={'cols': 80, 'rows': 20})})


