from rest_framework import serializers
from cart.models import WishList,CartItem,Order,Coupon,OrderCancel
from users.api.serializers import RegistrationsSerializer
from django.contrib.auth.models import User

class WishListSerializers(serializers.ModelSerializer):
	class Meta:
		model = WishList
		fields = ['user','ordered','is_product_available','item','wishlist_id',]


class CartItemSerializers(serializers.ModelSerializer):
	user = serializers.StringRelatedField(read_only=True)
	item = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = CartItem
		fields = ['user','ordered','item','quantity','cart_id']


class CouponSerializers(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['code','amount',]


class OrderCancelSerializers(serializers.ModelSerializer):
	class Meta:
		model = OrderCancel
		fields = ['order','reason','accepted','email',]


