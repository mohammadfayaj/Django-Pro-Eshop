from rest_framework import serializers
from blog.models import HeaderImage,BannerImage,BlogPost,Contact


class HeaderImageSerializers(serializers.ModelSerializer):
	class Meta:
		model = HeaderImage
		fields = ['titel','header_image',]


class BannerImageSerializers(serializers.ModelSerializer):
	class Meta:
		model = BannerImage
		fields = ['banner_title','banner_image','banner_image_1','banner_image_2',]


class BlogPostSerializers(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['blog_title','blog_description','blog_image','created_at','updated_at',]


class ContactSerializers(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = ['titel','shop_address','facebook','twitter','email','phone_number',]