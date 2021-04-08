from django.urls import path
from .import views 

app_name = "shop"

urlpatterns = [

    path('product-list/', views.Product_List, name='product_list'),
    path('size_/', views.SizeView, name='size'),
    path('product_details/<product_slug>/', views.product_details_and_review, name='product-details'),
    path('category/<category_list>/', views.Categories_List, name='category-list'),
    path('review/all/', views.ReviewList, name='review_all'),
    path('review/<int:id>/update/', views.ReviewUpdate, name='review_update'),
    path('review/<int:id>/delete/', views.ReviewDelete, name='review_delete'),

]































