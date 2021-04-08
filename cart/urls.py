from django.urls import path
from . import views
from django.conf.urls import url
# from notification import urls

app_name = "cart"

urlpatterns = [
    path('', views.AdminChart , name='chart'),
    path('cart_item/', views.CartListView, name='cart-list-view'),
     
    path('wishlist/', views.WishListView, name='wish_list'),
    path('wishlist/<slug>/', views.add_to_wishlist, name='add_wish_list'),
    path('wishlist_remove/<int:id>/', views.remove_to_wishlist, name='remove_wish_list'),


    
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),

    path('add_to_quantity/<slug>', views.add_to_quantity, name='add-to-quantity'),
    path('remove_quantity/<slug>', views.remove_from_quantity, name='remove-from-quantity'),

]



# path('inbox/', views.test_mark_all_as_unread_manager, name='mark'),
# url(r'^test_make/', views.make_notification),
# url(r'^test/', views.live_tester),
# path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
# path('cart-list-view/', views.cart_list_view, name='cart-list-view'),
