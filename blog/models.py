from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class HeaderImage(models.Model):
	titel = models.CharField(max_length=150, help_text = "This titel will appear in the Image")
	header_image = models.ImageField(upload_to="header_image")

	def __str__ (self):
		return self.titel

	def save(self):
		#Opening the uploaded image
		img = Image.open(self.header_image) # Open Image On The Fly

		if img.height > 1140 or img.width > 1140:
			# output = BytesIO() 

			#Resize/modify the image
			output_size = (1140, 1140)
			img.thumbnail(output_size)
			img = img.convert('RGB')

			output = BytesIO()
			#after modifications, save it to the output
			img.save(output, format='JPEG' ,quality=100)
			output.seek(0)

			#change the imagefield value to be the newley modifed image value
			self.header_image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.header_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(HeaderImage,self).save()



class BannerImage(models.Model):
	banner_title = models.CharField(max_length=60, default='Banner Image')
	banner_image = models.ImageField(upload_to="banner_image", help_text = "image height should be 240px or 300px")

	def __str__ (self):
		return self.banner_title

	def save(self):
		#Opening the uploaded image
		img = Image.open(self.banner_image) # Open Image On The Fly

		if img.height > 750 or img.width > 750:
			# output = BytesIO() 

			#Resize/modify the image
			output_size = (750, 750)
			img.thumbnail(output_size)
			img = img.convert('RGB')

			output = BytesIO()
			#after modifications, save it to the output
			img.save(output, format='JPEG' ,quality=100)
			output.seek(0)

			#change the imagefield value to be the newley modifed image value
			self.banner_image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.banner_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(BannerImage,self).save()


class BlogPost (models.Model):
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	blog_title = models.CharField(max_length=60)
	blog_description = models.TextField()
	blog_image = models.ImageField(upload_to="blog_image")
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

	def __str__ (self):
		return self.blog_title


	def save(self):
		#Opening the uploaded image
		img = Image.open(self.blog_image) # Open Image On The Fly

		if img.height > 600 or img.width > 600:
			# output = BytesIO() 

			#Resize/modify the image
			output_size = (500, 600)
			img.thumbnail(output_size)
			img = img.convert('RGB')

			output = BytesIO()
			#after modifications, save it to the output
			img.save(output, format='JPEG' ,quality=100)
			output.seek(0)

			#change the imagefield value to be the newley modifed image value
			self.blog_image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.blog_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(BlogPost,self).save()


class Contact(models.Model):
	titel = models.CharField(max_length=30, default='Contact')
	shop_address = models.CharField(max_length=150)
	facebook = models.CharField(max_length=150, help_text = "Place Your Facebook Account Url")
	twitter = models.CharField(max_length=150, help_text = "Place Your twitter Account Url")
	email = models.CharField(max_length=150, help_text = "Place Your Email")
	phone_number = PhoneNumberField(help_text='Please Enter Your Valid Phone Number.',)

	def __str__ (self):
		return self.titel
