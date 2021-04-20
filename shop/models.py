from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import truncatechars  # or truncatewords
from ast import literal_eval# literal_eval, turns your string into an actual list of tuples

from star_ratings.models import Rating
from users.models import Profile
import uuid

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from notifications.signals import notify

class Category(MPTTModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="category_pic", blank=True, null=True)
    parent = TreeForeignKey('self' , null=True, blank=True, related_name= 'children', db_index=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,db_index=True,help_text='Unique value for product page URL, created from name.')
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def category_save(self):
        if self.image is not None:
            #Opening the uploaded image
            img = Image.open(self.image) # Open Image On The Fly

            if img.height > 300 or img.width > 300:
                # output = BytesIO() 

                #Resize/modify the image
                output_size = (300, 300)
                img.thumbnail(output_size)
                img = img.convert('RGB')

                output = BytesIO()
                #after modifications, save it to the output
                img.save(output, format='JPEG' ,quality=100)
                output.seek(0)

                #change the imagefield value to be the newley modifed image value
                self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

            super(Category,self).save()
        else:
            super(Category,self).save()


AVAILABILITY = (

    ('In stock', 'In stock'),
    ('Out of stock', 'Out Of Stock')
)


COLORS = (

    ('White', 'White'),
    ('Gray',  'Gray '),
    ('Red',   'Red'),
    ('Black', 'Black'),
    ('Green', 'Green'),
    ('Blue',  'Blue'),

)

class ProductItem(models.Model,):
    titel = models.CharField(max_length=100, null=True)
    images = models.ImageField(upload_to="productitem_pic",)
    images_1 = models.ImageField(upload_to="productitem_pic", blank=True, null=True)
    images_2 = models.ImageField(upload_to="productitem_pic", blank=True, null=True)
    images_3 = models.ImageField(upload_to="productitem_pic", blank=True, null=True)
    meta_keywords = models.CharField("Meta keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', blank=True, null=True)      
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag' ,blank=True, null=True)

    description = models.TextField(blank=True,null=True)
    brand = models.CharField(max_length=50, blank=True,null=True)
    availability = models.TextField(blank=True, null=True,choices=AVAILABILITY, default='In stock')
    colors = models.TextField(blank=True, null=True, choices=COLORS)
    price = models.DecimalField(max_digits=9,decimal_places=2,null=True)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00) 
    
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_it_shirt = models.BooleanField(default=False,)
    is_it_Shoes = models.BooleanField(default=False)
    is_it_pant = models.BooleanField(default=False)

    quantity = models.IntegerField(null=True, help_text='How many product quantity do you have?') 
    date_added = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, default=uuid.uuid4,help_text='Unique value for product page URL, Auto genarated, But still if you want to Edit! You can.', null=True)
    categorys = TreeForeignKey(Category, blank=True, null=True , on_delete =models.CASCADE)
    ratings = GenericRelation(Rating, related_query_name='foos')


    def __str__(self):
        return self.titel

    class Meta:
        ordering = ['date_added']
        verbose_name_plural = 'Product Items'

    def sale_price(self):
        if self.old_price > self.price:
           return self.price
        else:
           return None 

    def get_absolute_url(self):
        return reverse("shop:product-details", kwargs={'product_slug': self.slug})
        #("appname:urls-name", kwargs={'custom_slug_name': self.slug}) 

    def colors_list(self):
        # literal_eval, turns your string into an actual list of tuples
        colors = literal_eval(self.colors)
        return colors

    def save(self):
        if self.images:
            #Opening the uploaded image
            img = Image.open(self.images) # Open Image On The Fly

            if img.height > 500 or img.width > 500:
                # output = BytesIO() 

                #Resize/modify the images
                output_size = (500, 500)
                img.thumbnail(output_size)
                img = img.convert('RGB')

                output = BytesIO()
                #after modifications, save it to the output
                img.save(output, format='JPEG' ,quality=100)
                output.seek(0)

                #change the imagesfield value to be the newley modifed images value
                self.images = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.images.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

            super(ProductItem,self).save()



class Reviews(MPTTModel):
    review = models.CharField(max_length=600)
    image = models.ImageField(upload_to="reviews_pic", blank=True, null=True)
    user_pic = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str((f"{self.user.username} Review This Product : **{self.product_item.titel}**"))
    
    class MPTTMeta:
        order_insertion_by = ['-created_date']

    class Meta:
        verbose_name_plural = 'Product Reviews By Customer'

    @property
    def reviews(self):
        #Reviw will only show 40 Alphabet in admin
        return truncatechars(self.review, 40)

    def save(self):
        super(Reviews,self).save()

        if self.image:
            #Opening the uploaded image
            img = Image.open(self.image) # Open Image On The Fly

            if img.height > 400 or img.width > 400:
                # output = BytesIO() 

                #Resize/modify the image
                output_size = (400, 400)
                img.thumbnail(output_size)
                img = img.convert('RGB')

                output = BytesIO()
                #after modifications, save it to the output
                img.save(output, format='JPEG' ,quality=100)
                output.seek(0)

                #change the imagefield value to be the newley modifed image value
                self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

            super(Reviews,self).save()
        










