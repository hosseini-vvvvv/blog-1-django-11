from dataclasses import fields
from email import message
from pyexpat import model
# >>>>> BALAYI HA KHODESH NEVESHTE  <<<<<<<
from django import forms
from .models import *


class AccountForm(forms.Form):
    GENDER_CHOICES = {
        ('اقا', 'اقا'),
        ('خانم', 'خانم')
    }
    phone=forms.CharField(max_length=11,required=True)
    name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    age=forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    address = forms.CharField(max_length=250, widget=forms.Textarea)



    def clean_phone(self):
        phone =self.cleaned_data["phone"]
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن باید عددی باشد")
            
            else:
                return phone

    def clean_age(self):
        age =self.cleaned_data["age"]
        if age:
            if age<0:
                raise forms.ValidationError("عدد سن نباید منفی باشد")
            
            else:
                return age



class ContactusForm(forms.Form):
    message=forms.CharField(widget=forms.Textarea,required=True)
    name=forms.CharField(max_length=25,required=True)
    email=forms.EmailField(required=True)
    subject=forms.CharField(required=True,max_length=25)
    phone=forms.CharField(max_length=11,required=False)
    
    
    
class shareForm(forms.Form):
    message=forms.CharField(widget=forms.Textarea(attrs={'class':'k'}),required=True)
    name=forms.CharField(max_length=25,required=True,widget=forms.TextInput(attrs={'class':'m'}))
    to=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'l'}))
    # widget=forms.Textarea(attrs={'class':'k'} >>>>>>>>  style dehi dar base.css

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','body')
            


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class ChangePasswordForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput())
    new_password1=forms.CharField(widget=forms.PasswordInput())
    new_password2=forms.CharField(widget=forms.PasswordInput())
    






