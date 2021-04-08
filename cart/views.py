from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Length, Upper
from django.db.models import Count, F, Value

from cart.models import CartItem,Coupon,Order,WishList
from cart.forms import CouponForm
from notifications.signals import notify
from shop.models import ProductItem

def AdminChart(request):
    template = 'admin/index.html'
    orders = Order.objects.filter(ordered=True).count()
    users = User.objects.all().count()

    context = {
     'orders' : orders,
     'users'  : users,
    }
    return render(request, template, context)

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("cart:cart-list-view")

@login_required
def WishListView(request):
    template = 'cart/wishlist.html'
    wishlist = WishList.objects.all()
    product = ProductItem.objects.filter(quantity__gt=1)

    try:
        wishlist = WishList.objects.filter(user=request.user, ordered=False)
    except ObjectDoesNotExist:
        pass
    empty_massage = "Your Wish list is empty"

    context = {
        'cart' : 'order',
        'wishlist' : wishlist,
        'empty_massage' : empty_massage,
        'product':product,
    }

    return render(request, template, context)


def add_to_wishlist(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(ProductItem, slug=slug)
        wish_item, created = WishList.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        wish_item.save()
    return redirect("shop:product_list")


def remove_to_wishlist(request, id):
    if request.user.is_authenticated:
        item = get_object_or_404(WishList, id=id, ordered=False, user=request.user)
        item.delete()
    return redirect("cart:wish_list")

@login_required
def CartListView(request):

    try:
        order = Order.objects.get(user=request.user, ordered=False,)
    except Order.DoesNotExist:
        order= None
    

    template = 'cart/shoping-cart.html'
    empty_massage = "Your Cart Is Empty, Please Keep Shopping..."

    form = CouponForm(request.POST or None)
    # deliverycharge = get_object_or_404(Deliverycharges, user=request.user)

    if form.is_valid():
        try:
            code = form.cleaned_data.get('code')
            order = Order.objects.get(
                user=request.user, ordered=False)
            order.coupon = get_coupon(request, code)
            # order.deliverycharge = deliverycharge
            order.save()
            messages.success(request, "Successfully added coupon")
            return redirect("cart:cart-list-view")

        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect("cart:cart-list-view")

    context = {
      'cart': order,
      'empty_massage': empty_massage,
      'ms':'ms',
      'form':form,
    }
    
    return render(request, template, context)


def add_to_cart(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(ProductItem, slug=slug)
        cart_item, created = CartItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False,
            is_active=True,

        )
        cart_item.save()
        order_qs = Order.objects.select_related().filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                # cart_item.quantity += 1
                # cart_item.save()
                messages.success(request, "This item was added to your cart.")
                return redirect("shop:product_list")
            else:
                order.items.add(cart_item)
                messages.success(request, "This item was added to your cart.")
                return redirect("shop:product_list")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, 
                ordered_date=ordered_date,
                )
            order.items.add(cart_item)

            # notify.send(user=request.user, recipient=user, verb='you reached level 10')
 
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:product_list")
    return redirect('cart:cart-list-view')


def remove_from_cart(request, slug):
    item = get_object_or_404(ProductItem, slug=slug)
    order_qs = Order.objects.select_related().filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.select_related().filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(cart_item)
            cart_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart:cart-list-view")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart:cart-list-view")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:cart-list-view")


def add_to_quantity(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(ProductItem, slug=slug)
        cart_item, created = CartItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False,
        )
        order_qs = Order.objects.select_related().filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                cart_item.quantity += 1
                cart_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("cart:cart-list-view")
            else:
                return redirect("cart:cart-list-view")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(cart_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart:cart-list-view")
    return redirect('cart:cart-list-view')


def remove_from_quantity(request, slug):
    item = get_object_or_404(ProductItem, slug=slug)
    order_qs = Order.objects.select_related().filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.select_related().filter(item=item,user=request.user,ordered=False)[0]
            if cart_item.quantity <= 1:
                cart_item.quantity == 1
                return redirect("cart:cart-list-view")
            else:
                cart_item.quantity -= 1
                cart_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:cart-list-view")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart:cart-list-view")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:cart-list-view")

