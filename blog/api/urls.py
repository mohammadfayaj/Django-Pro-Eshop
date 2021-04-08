from django.urls import path
from blog.api import views

urlpatterns = [
    path('headerimage/', views.header_image_list),
    path('bannerimage/', views.banner_image_list),
    path('blogpost/', views.blog_post_list),
    path('contact/', views.contact_list),

]