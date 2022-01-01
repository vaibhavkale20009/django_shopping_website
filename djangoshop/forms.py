from djangoshop.models import items
from django import forms

class itemform(forms.ModelForm):
    class Meta:
        model=items
        fields=('__all__')
