from django import forms
from models import user_details


class signedup(forms.ModelForm):
    class Meta:
        model = user_details
        fields = ['name','username','email','password']

class login_form(forms.ModelForm):
    class Meta:
        model=user_details
        fields = ['username','password']