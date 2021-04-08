from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
from django import template
import datetime

from checkout.models import CashOnDeliveryPaymentStatus,StripePaymentStatus
from shop.models import ProductItem
from cart.models import Order

register = template.Library()

#loaded admin/index.html
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


#loaded admin/index.html
@register.filter
def users(user):
 	if user.is_authenticated:
 		user = User.objects.all()
 		return user.count()

 
#loaded admin/index.html
@register.filter
def products(user):
	if user.is_authenticated:
		item = ProductItem.objects.all()
		return item.count()
	else:
		return 0
		
#loaded admin/index.html
@register.filter
def orders(user):
	if user.is_authenticated:
		order = Order.objects.all()
		return order.count()
	else:
		return 0

#loaded admin/index.html
@register.filter
def cash_on_deliverys(user):
	if user.is_authenticated:
		cash_on = CashOnDeliveryPaymentStatus.objects.all()
		return cash_on.count()
	else:
		return 0

#loaded admin/index.html
@register.filter
def payments (user):
	if user.is_authenticated:
		payment = StripePaymentStatus.objects.all()
		return payment.count()
	else:
		return 0


#loaded shop/shop-details.html
# @register.filter
# def reviewcount(review):
# 	review = ProductItem.objects.annotate(Count('reviews'))
# 	# review = product[0].reviews__count
# 	# review = Reviews.objects.all()
# 	return review
# {{ review|reviewcount }}

# {{product_details.reviews_set.all|length}}