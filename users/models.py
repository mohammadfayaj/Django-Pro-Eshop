from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from intl_tel_input.widgets import IntlTelInputWidget
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.urls import reverse


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.ImageField(default='default.jpg', upload_to="profile_pic",null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name_plural = 'Customer Profile'

DELIVERY = [

    ('Home', 'Home'),
    ('Office', 'Office')
]

class Devision(models.Model): #country
    devision = models.CharField(max_length=50)

    def __str__(self):
        return self.devision

class Deliverycharges(models.Model): #city
    user = models.ForeignKey(User, on_delete=models.CASCADE ,blank=True, null=True)
    division_in_charge = models.ForeignKey(Devision, on_delete=models.CASCADE, blank=True, null=True)
    delivery_charge = models.IntegerField(null=True,blank=True, default=0)    
    
    # def __str__(self):
    #     return f"{self.division_in_charge} Devision Delivary Charge {self.delivery_charge}$"

    class Meta:
        verbose_name_plural = 'Delivery Charge'

    def __str__(self):
        return str(self.delivery_charge)


class Address (models.Model): #persion
    users = models.ForeignKey(User, on_delete=models.CASCADE,)
    devision = models.ForeignKey(Devision, on_delete=models.CASCADE,null=True)
    deliverycharges = models.ForeignKey(Deliverycharges, on_delete=models.CASCADE, blank=True, null=True)

    phone_number = PhoneNumberField(help_text='Please Enter Your Valid Phone Number.',null=True)
    
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    house_number = models.CharField(max_length=32,help_text='Your Village Name And House Number',null=True)
    effective_delivery = models.CharField(max_length=30, choices=DELIVERY,default='Home',null=True)
    city = models.CharField(max_length=30,null=True)
    zone = models.CharField(max_length=30, blank=True, null=True)



    def __str__(self):
        return f'{self.users.username} Address'

    class Meta:
        verbose_name_plural = 'Customer Address'
        db_table = 'address'

    # def get_absolute_url_address(self):
    #     return reverse("users:users-address-info", kwargs={'id' : self.id} )






