from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from localusers import forms

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html",
         form_class=forms.AuthenticationForm,), name='login')
]
