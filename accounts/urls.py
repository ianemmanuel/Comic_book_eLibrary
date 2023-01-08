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
     path('<int:pk>/profile/', views.ShowProfilePageView.as_view(), name= 'show_profile_page'),
     path('<int:pk>/edit_profile_page/', views.EditProfilePageView.as_view(), name= 'edit_profile_page'),
     path('create_profile_page/', views.CreateProfilePageView.as_view(), name= 'create_profile_page'),
     path('my-dashboard',views.my_dashboard, name='my_dashboard'),
       # Wishlist
     path('add-wishlist',views.add_wishlist, name='add_wishlist'),
     path('my-wishlist',views.my_wishlist, name='my_wishlist'),
     #Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    path('my_shop', views.ViewPost.as_view(), name='my_shop'),

      
]
