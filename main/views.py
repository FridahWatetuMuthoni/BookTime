from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import ContactForm
from django.views.generic.edit import FormView
from main import models

# Create your views here.


class ProductListView(ListView):
    template_name = 'main/products_list.html'
    paginate_by = 4

    # we return the products filtered by active then by tag if the tag is specified and if not return all the active products
    # When an instance of this view is created, the attributes args and kwargs are populated with information from the URL route. In our case,
    # this view is expecting to be called with the tag specified in the URL path, rather than in a GET parameter. If, on the other hand, the tag were a GET
    # parameter, it could be accessed using the self.request.GET dictionary.
    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(models.ProductTag, slug=tag)
        if self.tag:
            products = models.Product.objects.active().filter(tags=self.tag)
        else:
            products = models.Product.objects.active()
        return products.order_by('name')


class ContactFormView(FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = '/'

# This function is callled if the form is valid
    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
