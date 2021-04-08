from rest_framework import serializers
from shop.models import Category,ProductItem,Reviews


class CategorySerializers(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['name','image','parent','slug','is_active', 'created_at', 'updated_at']

class ProductItemSerializers(serializers.ModelSerializer):
	ratings = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = ProductItem
		fields = ['titel','images','images_1','images_3','images_3', 'meta_keywords','meta_description',
		  'description','brand','availability', 'colors', 'price', 'old_price', 'is_active',
		  'is_bestseller', 'is_featured', 'is_it_shirt', 'is_it_Shoes', 'is_it_pant',
		  'quantity', 'date_added', 'slug', 'categorys', 'ratings'
		]

class ReviewsSerializers(serializers.ModelSerializer):
	class Meta:
		model = Reviews
		fields = ['review','image','user_pic','user','product_item','parent', 'created_date', 'updated_date','status',]
