import uuid

from django.db import models
from django.contrib.auth.models import User

PLACEHOLDER_PATH = "/media/images/placeholder.png"


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"Customer id: {self.id}, name: {self.first_name}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f"Product id: {self.id}, name: {self.name}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return PLACEHOLDER_PATH


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Ref: https://stackoverflow.com/a/4443212/6672398
    order_item = models.ManyToManyField(Product, through="OrderItem")

    def __str__(self):
        return f"Order id: {self.id}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        return sum([item.get_total for item in orderitems])

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shopping Address id: {self.id}"
