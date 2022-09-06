from distutils.command.upload import upload
from django.db import models

# Create your models here.


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)

    # This method will be availProduct.objects.active() to return only active products. To finish this
    objects = ActiveManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    # The product stores the primary key of the linked product model.It is used by the ORM to run JOIN operations automatically when accessed
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")
    thumbnail = models.ImageField(upload_to='product-thumbnails', null=True)

    def __self__(self):
        return self.product.name


class ProductTag(models.Model):
    # One product may have one or many tags, and one tag may contain one or more products
    products = models.ManyToManyField(Product, blank=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
