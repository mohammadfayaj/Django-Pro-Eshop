from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime
from datetime import datetime

class ConvertingDateTimeField(models.DateTimeField):

    def get_prep_value(self, value):
        return str(datetime.strptime(value, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")) 

class BkashPaymentStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    transation_status = models.CharField(max_length=50, blank=True, null=True)
    paymentId = models.CharField(max_length=50, null=True)
    trxId = models.CharField(max_length=50, null=True)
    merchant_invoice_number = models.CharField(max_length=80, null=True)
    amount = models.DecimalField(max_digits=11, default=0.00, decimal_places=2, null=True)
    currency = models.CharField(max_length=50, null=True, default='BDT')
    intent = models.CharField(max_length=50, null=True)
    # create_time = ConvertingDateTimeField(blank=True, null=True,)
    create_time = models.CharField(blank=True, null=True, max_length=100)

    update_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} Bkash PaymentID: {self.paymentId}"

    class Meta:
        verbose_name_plural = 'Bkash Payment Status'

class StripePaymentStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(blank=True, null= True,max_length=400)
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} Stripe Payment Token: {self.stripe_charge_id}"

    class Meta:
        verbose_name_plural = 'Stripe Payment Statement'


class CashOnDeliveryPaymentStatus(models.Model):
    Payment_statement = models.CharField(max_length=100,blank=True, null=True, default='Cash on delivery')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user} PaymentStatus: {self.Payment_statement}" 

    class Meta:
        verbose_name_plural = 'Cash On Delivery Payment Statement'








