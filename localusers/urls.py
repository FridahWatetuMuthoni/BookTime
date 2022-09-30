from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from localusers import forms

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="localusers/login.html",
         form_class=forms.AuthenticationForm,), name='login'),
    path('address/', views.AddressListView.as_view(), name='address_list'),
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('address/<int:pk>/', views.AddressUpdateView.as_view(),
         name='address_update'),
    path('address/<int:pk>/delete',
         views.AddressDeleteView.as_view(), name='address_delete')
]
