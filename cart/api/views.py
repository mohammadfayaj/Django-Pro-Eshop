from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



from cart.api.serializers import WishListSerializers,CartItemSerializers,CouponSerializers,OrderCancelSerializers
from cart.models import WishList,CartItem,Coupon,OrderCancel




@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def wish_list(request):
	if request.method == "GET":
		wish_object = WishList.objects.all()
		serializers = WishListSerializers(wish_object, many=True)
		return Response(serializers.data)
	return Response(serializers.errors, status=400)


@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def cart_list(request):
	if request.method == "GET":
		cart_object = CartItem.objects.all()
		serializers = CartItemSerializers(cart_object, many=True)
		data = {}
		data['user'] = request.user.username
		return Response(serializers.data)
	return Response(serializers.errors, status=400)


@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def coupon(request):
	if request.method == "GET":
		coupon_object = Coupon.objects.all()
		serializers = CouponSerializers(coupon_object, many=True)
		return Response(serializers.data)
	return Response(serializers.errors, status=400)


@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def order_cancel(request):
	if request.method == "GET":
		order_cancel_object = OrderCancel.objects.all()
		serializers = OrderCancelSerializers(order_cancel_object, many=True)
		return Response(serializers.data)
	return Response(serializers.errors, status=400)
