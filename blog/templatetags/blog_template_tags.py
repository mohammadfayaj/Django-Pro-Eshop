from django import template
from blog.models import Contact
from shop.models import ProductItem
from cart.models import CartItem,Order, WishList
from users.models import Address
from django.db.models import Count
# from django.contrib.deco
register = template.Library()

#loaded blog/base_navbar.html
@register.inclusion_tag('base/footer.html', takes_context=True)
def contact_global_query_data(context):
	contact_var = Contact.objects.all()
	return {'contact_var' : contact_var}

# loaded blog/base_navbar.html
@register.inclusion_tag('base/contact_base.html', takes_context=True)
def contact_global(context):
	contact_var = Contact.objects.all()
	return {'contact_var' : contact_var}

#load ajax.html
@register.filter
def subtract(value, arg):
    return value + arg

#loaded blog/home.html
@register.filter 
def sort_by_date(queryset, date_added):
    return ProductItem.objects.all().order_by(date_added)

#loaded blog/home.html
@register.filter
def sort_by_ratings(queryset, ratings):
    return ProductItem.objects.all().order_by(ratings)

# load base/base_navbar.html
@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        # return qs.count()
        # it take some much query time
        if qs.exists(): 
        	return qs [0].items.count()
        return 0
    else:
        return 0

# load base/base_navbar.html
@register.filter
def wish_item_count(user):
    if user.is_authenticated:
        qs = WishList.objects.filter(user=user, ordered=False)
        # return qs.count()
        # it take some much query time
        if qs.exists(): 
        	return qs.count()
        return 0
    else:
        return 0

from django.contrib.auth.decorators import login_required

# hit on base/base_navbar.html

@register.simple_tag
def cart_cost(user, quantity, item,):
    total = 0
    cart = CartItem.objects.select_related().filter(user=user, ordered=False) #select_related will help reduce query-set time
    for i in cart:
        var = i.quantity * i.item.price #item its a forignkey in CartItem model
        total += var
    return total

