from django.contrib import admin
from .models import BkashPaymentStatus, StripePaymentStatus, CashOnDeliveryPaymentStatus

# Register your models here.
admin.site.register(BkashPaymentStatus)
admin.site.register(StripePaymentStatus)
admin.site.register(CashOnDeliveryPaymentStatus)

