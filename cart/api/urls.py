from django.urls import path
from cart.api import views

urlpatterns = [
    path('wishlist/', views.wish_list),
    path('cartitem/', views.cart_list),
    path('coupon/', views.coupon),
    path('ordercancel/', views.order_cancel),

]