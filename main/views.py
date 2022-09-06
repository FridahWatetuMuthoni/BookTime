from django.shortcuts import render
from .forms import ContactForm
from django.views.generic.edit import FormView

# Create your views here.


class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

# This function is callled if the form is valid
    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
