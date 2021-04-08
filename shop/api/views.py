from rest_framework.decorators import api_view,permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.permissions import IsAuthenticated


from shop.api.serializers import CategorySerializers,ProductItemSerializers,ReviewsSerializers
from shop.models import Category,ProductItem,Reviews


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def category_response(request):
	if request.method == 'GET':
	    category = Category.objects.all()
	    serializer = CategorySerializers(category, many=True)
	    return Response(serializer.data)
	return Response(serializer.errors, status=400)


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def product_item_response(request):
	if request.method == "GET":
		product_item = ProductItem.objects.all()
		serializers = ProductItemSerializers(product_item, many=True)
		return Response(serializers.data)
	return Response(serializers.errors, status=400)


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def blog_post_list(request):
	if request.method == "GET":
		reviews = Reviews.objects.all()
		serializer = ReviewsSerializers(reviews, many=True)
		return Response(serializer.data)
	return Response(serializer.errors, status=400)

