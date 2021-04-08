from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
  
    path('address_info_/<int:id>/', views.check_out_view ,name='check-out'),
    path('payment_option_/', views.payment_option ,name='payment-options'),
    path ('Success_url/<int:id>/', views.success_page , name='success-page'),

    path('get_delivery_charges/',  views.get_ajax_data, name= 'get_ajax_data_load'),
    path('export_pdf/<int:id>/',  views.export_pdf, name= 'export_as_pdf'),

    path('stripe/', views.stripe_payment_view ,name='stripe-payment'),
    path ('cash_on_delivery/<int:id>/', views.cash_on_delivery , name='cash-on-process'),
    path('bkash/<int:id>/',views.Bkash, name='bkash_pyment'),
    path('paypal/', views.Paypal, name='paypal_payment'),
  
  ]
