from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.db import transaction
from .models import User,Customer,Employee, Profile

class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number=self.cleaned_data.get('phone_number')
        customer.location=self.cleaned_data.get('location')
        customer.save()
        return user

class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        employee = Employee.objects.create(user=user)
        employee.phone_number=self.cleaned_data.get('phone_number')
        employee.designation=self.cleaned_data.get('designation')
        employee.save()
        return user

class EditProfileForm(UserChangeForm):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
  first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
  last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
  username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
  # last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
  # is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
#   is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
  # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
  # date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))


  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email','password')

class PasswordChangingForm(PasswordChangeForm):
  old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
  new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
  new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))


  class Meta:
    model = User
    fields = ('old_password', 'new_password1', 'new_password2')


class ProfilePageForm(forms.ModelForm):
  class Meta:
    model= Profile
    fields = ('bio','profile_pic','facebook_url','instagram_url','twitter_url','website_url')
    widgets = {
      'bio': forms.Textarea(attrs={'class':'form-control'}),
      # 'profile_pic': forms.ImageField(attrs={'class':'form-control'}),
      'facebook_url': forms.TextInput(attrs={'class':'form-control'}),
      'instagram_url': forms.TextInput(attrs={'class':'form-control'}),
      'twitter_url': forms.TextInput(attrs={'class':'form-control'}),
      'website_url': forms.TextInput(attrs={'class':'form-control'}),

    }

class EditProfilePageForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields=('bio','profile_pic','facebook_url','instagram_url','twitter_url','website_url')
    widgets = {
      'bio': forms.Textarea(attrs={'class':'form-control'}),
      # 'profile_pic': forms.ImageField(attrs={'class':'form-control'}),
      'facebook_url': forms.TextInput(attrs={'class':'form-control'}),
      'instagram_url': forms.TextInput(attrs={'class':'form-control'}),
      'twitter_url': forms.TextInput(attrs={'class':'form-control'}),
      'website_url': forms.TextInput(attrs={'class':'form-control'}),
    }