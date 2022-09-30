from django.shortcuts import render
from django.urls import reverse_lazy
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm
from . import models


# Create your views here.


logger = logging.getLogger(__name__)


class SignUpView(FormView):
    template_name = 'localusers/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_invalid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(f'New Signup for email {email}')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, 'You have signup successfully')
        return response

# Giving customers the ability to change and delete there addresses
# We are going to use  these class-based views: ListView, CreateView, UpdateView, and DeleteView.
# The LoginRequieredMixin is used to make sure the this views are only seen when logged in


class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address

    def get_queryset(self):
        # only getting the address belonging to the customer
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'country']
    success_url = reverse_lazy("address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'country']
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
