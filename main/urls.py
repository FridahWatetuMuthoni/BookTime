from django.urls import path
from django.views.generic import TemplateView, DetailView
from .views import ContactFormView, ProductListView, add_to_basket, manage_basket, AddressSelectionView
from main import models
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", TemplateView.as_view(template_name="main/home.html"), name='home'),
    path("about/", TemplateView.as_view(template_name="main/about.html"), name='about'),
    path("contact/", ContactFormView.as_view(), name='contact'),
    path('products/<slug:tag>/', ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/',
         DetailView.as_view(model=models.Product), name='product'),
    path('add_to_bascket/', add_to_basket, name='add_to_basket'),
    path('basket/', manage_basket, name="basket"),
    path('order/done', TemplateView.as_view(template_name='main/order_done.html'),
         name="checkout_done"),
    path('order/address_select/',
         AddressSelectionView.as_view(), name='address_select')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
