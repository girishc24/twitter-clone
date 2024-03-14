from django import forms
from .models import *

class MeepForm(forms.ModelForm):
    body=forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={"placeholder":"Enter Musker Meep", "class":"form-control", }), label="", )
    

    class Meta:
        model = Meep
        exclude = ("user",)