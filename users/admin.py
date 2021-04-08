from django.contrib import admin
from .models import *


class DeliverychargesAdmin(admin.ModelAdmin):
	fields = ['user', 'division_in_charge','delivery_charge',]

	list_display = ['user', 'division_in_charge', 'delivery_charge']



admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Devision)
admin.site.register(Deliverycharges, DeliverychargesAdmin)