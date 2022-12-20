from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from .form import CustomerSignUpForm, EmployeeSignUpForm, EditProfileForm,PasswordChangingForm,ProfilePageForm, EditProfilePageForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views import generic
from django.shortcuts import get_object_or_404, render


def register(request):
    return render(request, '../templates/register.html')

class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = '../templates/customer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = '../templates/employee_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


class UserEditView(UpdateView):
    form_class = EditProfileForm
    template_name = '../templates/edit_profile.html'
    success_url= '/'

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
  form_class = PasswordChangingForm
  # form_class = PasswordChangeForm
  success_url = reverse_lazy('password_success')
  # success_url = reverse_lazy('login')

def password_success(request):
  return render(request, '../templates/password_success.html',{})


class ShowProfilePageView(DetailView):
  model = Profile
  template_name = '../templates/user_profile.html'

  def get_context_data(self, *args, **kwargs):
    # users = Profile.objects.all()
    context = super(ShowProfilePageView, self).get_context_data(*args,**kwargs)
    page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
    context["page_user"] = page_user
    return context

class EditProfilePageView(generic.UpdateView):
  model = Profile
  template_name = '../templates/edit_profile_page.html'
  form_class =  EditProfilePageForm

  success_url = reverse_lazy('/')

class CreateProfilePageView(CreateView):
  model = Profile
  template_name = '../templates/create_user_profile_page.html'
  form_class = ProfilePageForm
  success_url = reverse_lazy('/')


  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)