from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Human, BiorythmsModel
from django.forms import ModelForm


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)
    #phone = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
       #user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class HumanForm(ModelForm):
    class Meta:
        model = Human
        fields = ['name', 'surname', 'email', 'phone', 'age', 'gender', 'height', 'weight']

class BiorythmsForm(ModelForm):
    class Meta:
        model = BiorythmsModel
        fields = ['birth_date', 'calculate_date']
