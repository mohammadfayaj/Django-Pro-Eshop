from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
from django.contrib.auth.models import User
from django.contrib import admin

from cart.models import Order,CartItem
from shop.models import ProductItem,Reviews,Category


# admin.site.site_header = "Ogani Eshop"
from django.db.models import Count
class ShopAdmin(admin.ModelAdmin):
    fields = (
              ('is_active','is_bestseller','is_featured','is_it_shirt','is_it_Shoes','is_it_pant'),
              ('titel'),('images'),('images_1'),('images_2'),('images_3'),('description'),('categorys'),('availability'),('colors'),
              ('brand'),('price'),('old_price'),('quantity'),
              ('date_added'),('meta_keywords'), ('meta_description'),('slug'),
              )
    list_display = [
                    'titel',
                    'categorys',
                    'price',
                    'quantity',
                    'availability',
                    'is_active',
                    'date_added',
                    ]
    
    # list_display_links = [
    #     'user',
    #     # 'total_product_item',
    # ]

    list_filter = ['date_added', 'colors', 'categorys', 'availability','titel',]

    search_fields = [
        'titel',
        'brand',
    ]

    # list_editable = ['items']

    # def total_product_item(self, obj):
    #     for i in obj.items.all():
    #         return (str(i.pk))


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','created_at')
    list_filter = ('created_at',)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'review' ,'created_date']


admin.site.register(ProductItem,ShopAdmin)
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Reviews,DraggableMPTTAdmin, 
                    list_display = ('tree_actions','indented_title', 'reviews' ,'created_date'), 
                    list_display_links= ('indented_title',),
                    expand_tree_by_default = True,)





























# from .forms import ProductAdminForm
# from django import forms

# #first create a custom form to use in admin
# class ProductAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ProductAdminForm, self).__init__(*args, **kwargs)
#         print (self.instance)
#         try:
#             #Try and set the selected_cat field from instance if it exists
#             self.fields['selected_cat'].initial = self.instance.subcategory.category.id
#         except:
#             pass
#     #The product model is defined with out the category, so add one in for display
#     category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), widget=forms.Select(attrs={'id':'category'}), required=False)
#     #This field is used exclusively for the javascript so that I can select the 
#     #correct category when editing an existing product
#     selected_cat = forms.CharField(widget=forms.HiddenInput, required=False)

#     class Meta:
#         model = Product
#         fields = ['name']

#     class Media:
#         #Alter these paths depending on where you put your media 
#         js = (
#             'js/MooTools-Core-1.6.0.js',
#             'js/admin.js',
#         )

# class ProductAdmin(admin.ModelAdmin):
#     form = ProductAdminForm
#     #I don't like using a fieldset here, because it makes the form more brittle,
#     #if you change the model for form be sure to update the fieldset.
#     #I'm using it in this instance because I need for category to show up 
#     #right above the subcategory
#     fieldsets = (
#         (None, {
#             'fields' : ('name','status','category','subcategory','description')
#         }),
#         ('Optional', {
#             'classes' : ('collapse',),
#             'fields' : ('brand','manufacturer','short_description','part_number','model_number','image','image_thumbnail','selected_cat')
#         })
#     )

# admin.site.register(Product, ProductAdmin)









# Register your models here.

# class ProductAdmin(admin.ModelAdmin):
#     form = ProductAdminForm
#     #I don't like using a fieldset here, because it makes the form more brittle,
#     #if you change the model for form be sure to update the fieldset.
#     #I'm using it in this instance because I need for category to show up 
#     #right above the subcategory
#     # fieldsets = (
#     #     (None, {
#     #         'fields' : ('titel',)
#     #     }),
#     #     ('Optional', {
#     #         'classes' : ('collapse',),
#     #         'fields' : ('images','categorys','sub_categorys','availability','price','old_price','quantity', 'categorys_node')
#     #     })
#     # )



# admin.site.site_header = "Ogani Eshop"


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     list_filter = ('created_at',)
#     # change_list_template = "shop/change_form.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('getSubcategory/', views.get_subcategory)
#         ]
#         return custom_urls + urls
        
#     def get_subcategory(request):
#         id = request.GET.get('id', '')
#         result = list(SubCategory.objects.filter(
#         category_id=int(id)).values('id', 'name'))
#         return HttpResponse(json.dumps(result), content_type="application/json")




# admin.site.register(ProductItem, ProductAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(SubCategory)
# admin.site.register(Category)

        # id = request.GET.get('id', '')
        # result = list(SubCategory.objects.filter(
        # category_id=int(id)).values('id', 'name'))
        # return HttpResponse(json.dumps(result), content_type="application/json")