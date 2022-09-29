from django.shortcuts import render
from django.urls import reverse
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import UserCreationForm


# Create your views here.


logger = logging.getLogger(__name__)


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm

    def get_success_url(self):
        #redirect_to = self.request.GET.get("next", "/")
        # return redirect_to
        return '/'

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
