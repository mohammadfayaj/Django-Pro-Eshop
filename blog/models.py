from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

class HeaderImage(models.Model):
	titel = models.CharField(max_length=150, help_text = "This titel will appear in the Image")
	header_image = models.ImageField(upload_to="header_image")

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.header_image.path)

		if img.height > 300 or img.width > 300:
			output_size = (1140, 1140)
			img.thumbnail(output_size)
			img.save(self.header_image.path)



	def __str__ (self):
		return self.titel


class BannerImage(models.Model):
	banner_title = models.CharField(max_length=60, default='Banner Image')
	banner_image = models.ImageField(upload_to="banner_image", help_text = "image height should be 240px or 300px")

	def __str__ (self):
		return self.banner_title

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.banner_image.path)

		if img.height > 300 or img.width > 300:
			output_size = (750, 240)
			img.thumbnail(output_size)
			img.save(self.banner_image.path)


class BlogPost (models.Model):
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	blog_title = models.CharField(max_length=60)
	blog_description = models.TextField()
	blog_image = models.ImageField(upload_to="blog_image")
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

	def __str__ (self):
		return self.blog_title


	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.blog_image.path)

		if img.height > 300 or img.width > 300:
			output_size = (500, 600)
			img.thumbnail(output_size)
			img.save(self.blog_image.path)


class Contact(models.Model):
	titel = models.CharField(max_length=30, default='Contact')
	shop_address = models.CharField(max_length=150)
	facebook = models.CharField(max_length=150, help_text = "Place Your Facebook Account Url")
	twitter = models.CharField(max_length=150, help_text = "Place Your twitter Account Url")
	email = models.CharField(max_length=150, help_text = "Place Your Email")
	phone_number = PhoneNumberField(help_text='Please Enter Your Valid Phone Number.',)

	def __str__ (self):
		return self.titel
