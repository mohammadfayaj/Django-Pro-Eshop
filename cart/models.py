from django.db import models
from django.utils import timezone
from django.urls import reverse
from shop.models import ProductItem
from users.models import Address, Deliverycharges
from django.contrib.auth.models import User
from notifications.signals import notify
from checkout.models import BkashPaymentStatus,StripePaymentStatus,CashOnDeliveryPaymentStatus
import shortuuid
import uuid
import random


class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    is_product_available = models.BooleanField(default=False)
    item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, null=True)
    wishlist_id  = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.user} want {self.item.titel}"

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True)
    cart_id  = models.CharField(max_length=250, null=True, blank=True,unique=True,default=shortuuid.uuid)

    def __str__(self):
        return f"{self.quantity} quantity of {self.item.titel}"

    class Meta:
        verbose_name_plural = 'Customer Shopping Cart Item'

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    items = models.ManyToManyField(CartItem)
    shipping_address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True,blank=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    deliverycost = models.ForeignKey(Deliverycharges, on_delete=models.SET_NULL, blank=True, null=True)
    
    cash_on_delivery = models.ForeignKey(CashOnDeliveryPaymentStatus, on_delete = models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(StripePaymentStatus, on_delete = models.SET_NULL, blank=True, null=True)
    bkash = models.ForeignKey(BkashPaymentStatus, on_delete=models.SET_NULL, blank=True, null=True)

    subtotal = models.DecimalField(decimal_places=2,max_digits=50, default=0.00,null=True,blank=True)
    ordered_date = models.DateTimeField()
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)

    shoes_size = models.CharField(max_length=255, help_text='', blank=True, null=True)
    shirt_size = models.CharField(max_length=255, help_text='', blank=True, null=True)
    pant_size = models.CharField(max_length=255, help_text='', blank=True, null=True)

    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    is_order_cancel = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    order_number = models.CharField(max_length=250,blank=True, null=True, editable=False, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-ordered']
        verbose_name_plural = 'Customer Order'

    def total_product(self,):
        return self.items.count()

    # goes to checkout/export-pdf.html
    def total(self):
        total = 0
        for i in self.items.all():
            total += i.get_total_item_price()
        return total

    #goes to cart/shoping-cart.html
    def show_cart_list_total(self):
        total = 0
        for i in self.items.all():
            total += i.get_total_item_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.coupon:
            total -= self.coupon.amount
            self.save()
        if self.deliverycost:
            total += self.deliverycost.delivery_charge
            self.save()
        return total
        # return f" $ {total}"

    def get_absolute_url(self):
        return reverse("checkout:cash-on-process", kwargs={'id': self.id})
        #("appname:urls-name", kwargs={'custom_slug_name': self.slug}) 


class Coupon(models.Model):
    code = models.CharField(max_length=15, help_text='')
    amount = models.DecimalField(decimal_places=2,max_digits=50, default=0.00,null=True,blank=True)
   
    def __str__(self):
        return self.code.upper()

ORDER_CHANGE_OPTION = (

    ('CHANGE MY MIND', 'CHANGE MY MIND'),
    ('OTHER REASON', 'OTHER REASON')
)


class OrderCancel(models.Model):
    order = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True, choices=ORDER_CHANGE_OPTION, default='CHANGE MY MIND')
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name_plural = 'Order Cancel By Customer'


