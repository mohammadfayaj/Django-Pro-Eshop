from django.urls import path
from .import views

app_name = "blog"

urlpatterns = [
    
    path('', views.Product_List, name='blog-home'),
    
    path('product_ds/<product_slug>/', views.Product_Details, name='product-details'),
    path('catory/<category_list>/', views.Categories_List, name='category-list'),
    
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.blog_details, name='blog-details'),

    path('developer/api/', views.api_view, name='api-view'),

    path('contact/', views.shop_contact, name='contact'),

  
]



