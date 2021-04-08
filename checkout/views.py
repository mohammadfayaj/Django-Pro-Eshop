from django.utils import timezone
from django.template.loader import render_to_string
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count ,F , Value, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from decimal import Decimal
from urllib3 import PoolManager

import datetime
import json
import requests
import stripe

import tempfile
from qr_code.qrcode.utils import QRCodeOptions
from weasyprint import HTML, CSS

from cart.models import Order,CartItem,WishList
from shop.models import ProductItem
from users.forms import AddressForm, DeliveryChargesForm
from users.models import Deliverycharges,Address
from checkout.models import BkashPaymentStatus,StripePaymentStatus,CashOnDeliveryPaymentStatus

from decouple import config
stripe.api_key = config('stripe.api_key') 


@login_required
def payment_option(request):
    template = 'checkout/payment.html'
    order = Order.objects.filter(user=request.user, ordered=False)
    return render(request, template, {'order':order})

def success_page(request,id):
    template = 'checkout/order_success_page.html'
    order = Order.objects.get(user=request.user,id=id)
    return render(request, template, {'order': order})

def get_ajax_data(request):
    division_in_charge_id = request.GET.get('devision') #devision variable
    order = Order.objects.get(user=request.user, ordered=False,)
    deliverycharges = Deliverycharges.objects.filter(division_in_charge_id = division_in_charge_id).order_by('delivery_charge')
    # division_in_charge [division_in_charge_id] is a foreignkey in Deliverycharges model that's link to the Devision Model
    context = {
        'deliverycharges' : deliverycharges,
        'order' : order
    }
    return render (request, 'checkout/ajax.html',  context)


def get_deliverycharges(request, delivery_charge):
    try:
        d_charge = Deliverycharges.objects.get(delivery_charge=delivery_charge,)
        # get delivery_charge field in DeliveryCharges Models
        return d_charge
    except ObjectDoesNotExist:
        messages.info(request, "This charge does not exist")
        return redirect("cart:cart-list-view")

@login_required
def check_out_view(request, id):
    order = Order.objects.get(user=request.user, ordered=False, id=id)
    address_info_list = Address.objects.filter(users=request.user)
    address_qs = Address.objects.get(users=request.user,)

    if request.method == "POST":
        address_info_form = AddressForm(request.POST, instance=address_qs)
        if address_info_form.is_valid():
            address_info_form.save()
            try:
                code = address_info_form.cleaned_data.get('deliverycharges')# deliverycharges foreigkey in Address Model.
                order = Order.objects.get(user=request.user, ordered=False, id=id)
                order.deliverycost = get_deliverycharges(request, str(code))
                # deliverycost is foreignkey in Order Model.
                order.save()
                messages.success(request, "Successfully added Deliverycharge")
                return redirect('checkout:payment-options')

            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order")
                return redirect('checkout:payment-options')

            address_info_form.save()

            return redirect('checkout:payment-options')
    else:
        address_info_form = AddressForm(instance = address_qs)

    context = {
        "address_info_list": address_info_list,
        "address_info_form": address_info_form,
        'order':order,
        'address_qs':'address_qs',
    }

    return render(request, 'checkout/checkout.html', context)



def get_quantity_update(request, slug, cart_id):
    try:
        cart_item = CartItem.objects.filter(user=request.user,is_active=True, cart_id=cart_id)
        product = ProductItem.objects.filter(slug=slug)

        for i in cart_item:
                cart_quantity = i.quantity
                product_quantity = i.item.quantity # item is a foreignkey in CartItem [ item indicated ProductItem model ] 
                result = product_quantity - cart_quantity
                product.update(quantity=result)

    except ObjectDoesNotExist:
        return HttpResponse('Something Bad Happened!')


@login_required
def Bkash(request, id):
    order = Order.objects.get(user= request.user, ordered = False, id=id)
    shipping_address = Address.objects.get(users=request.user)

    # update ProductItem model quantity field 
    for i in CartItem.objects.filter(user=request.user, is_active=True):
        slug = i.item.slug
        cart_id = i.cart_id
        get_quantity_update(request, slug, cart_id) # call get_quantity_update function

    if request.method == "POST" or request.is_ajax():
        receive_ajax = request.GET.get('data_set', None)
        json_data = json.loads(request.body.decode('utf-8'))
        
        # 'data_set' is a key, that hold all values & keys like 'paymentId' is a key
        paymentid = json_data['data_set']['paymentID']
        transactionStatus = json_data['data_set']['transactionStatus']
        merchant_invoice_number = json_data['data_set']['merchantInvoiceNumber']
        transactionStatus = json_data['data_set']['transactionStatus']
        amount = json_data['data_set']['amount']
        trx_id = json_data['data_set']['trxID']
        intent = json_data['data_set']['intent']
        create_time = json_data['data_set']['createTime']
        update_time = json_data['data_set']['updateTime']

        # create new BkahsPaymentStatus model
        bkash_create = BkashPaymentStatus(
            user = request.user,
            paymentId=paymentid,
            transation_status=transactionStatus,
            amount = amount,
            merchant_invoice_number = merchant_invoice_number,
            trxId = trx_id,
            intent = intent,
            create_time = create_time,
            # update_time = update_time,

            )
        bkash_create.save()

        # assign the models to the order
        order_items = order.items.all() # items it's a foreignkey connect to the CartItem model
        order_items.update(ordered=True)
        for item in order_items:
            item.save() # save cartitem
        order.ordered = True
        order.bkash = bkash_create # assign BkashPaymentStatus model to Order model
        order.shipping_address = shipping_address # assign Address model to Order model
        sub = order.sub_total() # calling def funtion form Order models to calculate the subtotal price
        order.subtotal = sub # subtotal is a field in Order models, here we assign [sub] variable value to the subtotal field 
        order.save()

        return JsonResponse(json_data , safe=False)

    context = {'order': order,}

    return render(request, 'checkout/bkash.html' ,context)


@login_required
def stripe_payment_view(request):
    order = Order.objects.get(user= request.user, ordered = False)
    token = request.POST.get('stripeToken')
    shipping_address = Address.objects.get(users=request.user)

    # update ProductItem model quantity field 
    for i in CartItem.objects.filter(user=request.user, is_active=True):
        slug = i.item.slug
        cart_id = i.cart_id
        get_quantity_update(request, slug, cart_id) # call get_quantity_update function

    try:
        # charge once off on the token
        charge = stripe.Charge.create(
            amount= int(order.sub_total() * 100),
            currency = 'usd',
            description = 'Pyment',
            source = token,
        )

        # create the payment
        payment = StripePaymentStatus()
        payment.stripe_charge_id = charge['id']
        payment.user = request.user
        payment.amount = order.sub_total()
        payment.save()

        # assign the payment to the order
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()
        order.ordered = True
        order.payment = payment
        order.shipping_address = shipping_address
        # order.ref_code = create_ref_code()
        order.save()

        messages.success(request, "Your order was successful!")
        return redirect('checkout:success-page')

    except stripe.error.CardError as e:

        body = e.json_body
        err = body.get('error', {})
        messages.warning(self.request, f"{err.get('message')}")
        return redirect("/")
        # messages.info(request, "")

    except stripe.error.RateLimitError as e:
        messages.info(request, "Too many requests hit the API too quickly. We recommend an exponential backoff of your requests.")

    except stripe.error.InvalidRequestError as e:
        messages.info(request, "The request was unacceptable, often due to missing a required parameter.")

    except stripe.error.AuthenticationError as e:
        messages.info(request, "Authentication with Stripe's API failed, Maybe you changed API keys recently")

    except stripe.error.APIConnectionError as e:
        messages.info(request, "Too many requests hit the API too quickly. We recommend an exponential backoff of your requests.")

    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        messages.info(request, "")

    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        messages.info(request, "Something went wrong on Stripe's end")

    context = {'cart': order}

    return render(request, 'checkout/stripe.html', context)


@login_required
def cash_on_delivery(request, id):
    template = 'checkout/order_success_page.html'

    # update ProductItem model quantity field 
    for i in CartItem.objects.filter(user=request.user, is_active=True):
        slug = i.item.slug
        cart_id = i.cart_id
        get_quantity_update(request, slug, cart_id) # call get_quantity_update function

    shipping_address = Address.objects.get(users=request.user)
    order = Order.objects.get(user=request.user, id=id)

    order_item = order.items.all() # items is a ForeignKey in Order model indicated CartItem model
    order_item.update(ordered=True, is_active=False) # update ordered field in CartItem model
    order.ordered = True # we set ordered field to True

    cash_on_delivery_create = CashOnDeliveryPaymentStatus() # Create full model objects
    cash_on_delivery_create.user = request.user 
    cash_on_delivery_create.save()

    order.shipping_address = shipping_address
    sub = order.sub_total() # calling def funtion form Order models to calculate the subtotal price
    order.subtotal = sub # subtotal is a field in Order models, here we assign [sub] variable value to the subtotal field
    order.cash_on_delivery = cash_on_delivery_create # cash_on_delivery is a ForeignKey in Order models 
    order.save()


    messages.info(request, f'Cash On delivary Order from {order.user.username} ')

    context= {'order': order,}
    return render(request, template, context )


def Paypal(request):
    order = Order.objects.get(user=request.user)
    return render(request,'checkout/paypal.html', {'cart': order})

def export_pdf(request, id):
    # template = 'checkout/export-pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inlineattachment; filename=Expenses' + str(datetime.datetime.now())+ '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    order = Order.objects.get(user=request.user, ordered=True, id=id)
    # cartitem = CartItem.objects.filter(user=request.user, ordered=True,)

    context = {'order' : order,}

    html_string = render_to_string('checkout/export-pdf.html' , context)
    html = HTML(string = html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

    # return render(request, template, context)
