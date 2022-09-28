from django.urls import path
from django.views.generic import TemplateView, DetailView
from .views import ContactFormView, ProductListView
from main import models
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", TemplateView.as_view(template_name="main/home.html"), name='home'),
    path("about/", TemplateView.as_view(template_name="main/about.html"), name='about'),
    path("contact/", ContactFormView.as_view(), name='contact'),
    path('products/<slug:tag>/', ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/',
         DetailView.as_view(model=models.Product), name='product')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
