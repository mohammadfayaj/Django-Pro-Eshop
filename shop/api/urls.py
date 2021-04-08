from django.urls import path
from shop.api import views

urlpatterns = [
    path('category/', views.category_response),
    path('productitem/', views.product_item_response),
    path('reviews/', views.blog_post_list),
    
]