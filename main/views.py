from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import ContactForm, BasketLineFormSet, AddressSelectionForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
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


def add_to_basket(request):
    product = get_object_or_404(
        models.Product, pk=request.GET.get("product_id"))
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = models.Basket.objects.create(user=user)
        request.session["basket_id"] = basket.id
    basketline, created = models.BasketLine.objects.get_or_create(
        basket=basket, product=product)
    if not created:
        basketline.quantity += 1
        basketline.save()
    return HttpResponseRedirect(reverse("product", args=(product.slug,)))


def manage_basket(request):
    if not request.basket:
        return render(request, "main/basket.html", {"formset": None})
    if request.method == "POST":
        formset = BasketLineFormSet(request.POST, instance=request.basket)
        if formset.is_valid():
            formset.save()
    else:
        formset = BasketLineFormSet(instance=request.basket)
    if request.basket.is_empty():
        return render(request, "main/basket.html", {"formset": None})
    return render(request, "main/basket.html", {"formset": formset})


class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = "localusers/address_select.html"
    form_class = AddressSelectionForm
    success_url = reverse_lazy('checkout_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)
