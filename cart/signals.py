from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from notifications.signals import notify
from cart.models import *

# @receiver(post_save, sender=User)
# def my_handler(sender, instance, created, **kwargs):
#     if created:
#         CartItem.objects.create(ordered=False,user=instance)
#         print('User my_handler ..........!')
#         notify.send(user=instance,verb='was saved')

# def my_handler(sender, instance, created, **kwargs):
# 	if created:
# 		CartItem.objects.create(user=instance)
# 		notify.send(user=instance,verb='was saved')

# post_save.connect(my_handler, sender=CartItem)

# @receiver(post_save, sender=CartItem)
# def my_handler(sender, instance, created, **kwargs):
#     # if created:
# 	   #  CartItem.objects.create()
# 	   #  print('User my_handler ..........!')
# 	notify.send(instance, verb='you reached level 10')

# post_save.connect(my_handler, sender=CartItem)


# @receiver(post_save, sender=Order)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Order.objects.create()
#         print('User Created ..........!')