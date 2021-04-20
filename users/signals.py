from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Address

from django.conf import settings
from rest_framework.authtoken.models import Token

from notifications.signals import notify
from shop.models import ProductItem


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('User Created ..........!')

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print('user Updated.........!')
 

@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
	if created:
		address_create = Address.objects.create(users=instance)
		address_create.save()
		print("Address Created........!")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_aut_token(sender, instance=None, created=False , **kwargs):
    if created:
    	Token.objects.create(user=instance)
    print('user token created.........!')
