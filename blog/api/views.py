from rest_framework.decorators import api_view,permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.permissions import IsAuthenticated


from blog.api.serializers import HeaderImageSerializers,BannerImageSerializers,BlogPostSerializers,ContactSerializers
from blog.models import HeaderImage,BannerImage,BlogPost,Contact


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def header_image_list(request):
	if request.method == 'GET':
	    header_image = HeaderImage.objects.all()
	    serializer = HeaderImageSerializers(header_image, many=True)
	    return Response(serializer.data)
	return Response(serializer.errors, status=400)


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def banner_image_list(request):
	if request.method == "GET":
		banner_image = BannerImage.objects.all()
		serializer = BannerImageSerializers(banner_image, many=True)
		return Response(serializer.data)
	return Response(serializer.errors, status=400)


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def blog_post_list(request):
	if request.method == "GET":
		blog_post = BlogPost.objects.all()
		serializer = BlogPostSerializers(blog_post, many=True)
		return Response(serializer.data)
	return Response(serializer.errors, status=400)


@api_view(["GET",])
@permission_classes([IsAuthenticated,])
def contact_list(request):
	if request.method == 'GET':
		contact = Contact.objects.all()
		serializer = ContactSerializers(contact, many=True)
		return Response(serializer.data)
	return Response(serializer.errors, status=400)
