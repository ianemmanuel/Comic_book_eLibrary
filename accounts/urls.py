from django.urls import path
from .import  views
from django.contrib.auth import views as auth_views

urlpatterns=[
     path('register/',views.register, name='register'),
     path('customer_register/',views.customer_register.as_view(), name='customer_register'),
     path('employee_register/',views.employee_register.as_view(), name='employee_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('edit_profile/',views.UserEditView.as_view(), name='edit_profile'),
     path('password/', views.PasswordsChangeView.as_view(template_name='../templates/change-password.html')),
      path('password_success', views.password_success, name="password_success"),
]
