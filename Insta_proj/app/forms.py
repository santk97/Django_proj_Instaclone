from django import forms
from models import user_details , post_model , likes


class signedup(forms.ModelForm):
    class Meta:
        model = user_details
        fields = ['name','username','email','password']

class login_form(forms.ModelForm):
    class Meta:
        model=user_details
        fields = ['username','password']


class posts(forms.ModelForm):
    class Meta:
        model = post_model
        fields=['image','caption']

class like(forms.ModelForm):
    class Meta:
        model = likes
        fields=['post']
