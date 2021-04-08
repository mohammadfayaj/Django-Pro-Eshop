from django.contrib import admin
from .models import *
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import Group, User
from django.contrib.admin import AdminSite

admin.site.unregister(Group)

class OrderAdmin(admin.ModelAdmin):
    change_form_template = "admin/order_change_form.html"
    fields = (

              ('ordered','is_order_cancel','being_delivered','received','refund_requested','refund_granted'),
              ('user'),('shipping_address'),('items'),('payment'),('cash_on_delivery'),('bkash'), ('shoes_size'),('shirt_size'),('pant_size'),
              ('coupon'),('ref_code'),('ordered_date'),('deliverycost'),
              ('subtotal'),

              )
    list_display = ['user',
                    'ordered_date',
                    # 'sub_total',
                    'total_product',
                    'ordered',
                    'being_delivered',
                    'received',
                    'is_order_cancel',
                    'refund_requested',
                    'refund_granted',
                    ]

    list_display_links = [
        'user',
        # 'total_product_item',
    ]

    list_filter = ['ordered','user', 'ordered_date']

    search_fields = [
        'user__username',
    ]

    # raw_id_fields = ['user']

    # list_editable = ['ordered',]

class CartAdmin(admin.ModelAdmin):
    fields = ('user','quantity', 'item','ordered','is_active','cart_id',)
    list_display = ['user',
                    'item',
                    'quantity',
                    # 'update',
                    'is_active',
                    'ordered',
                    ]

    # list_editable = ['ordered',]

# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon)
admin.site.register(CartItem, CartAdmin)
admin.site.register(WishList)




