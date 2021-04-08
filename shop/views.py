from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from .filters import ProductFilter
from django.utils import timezone
from star_ratings.models import *

from shop.forms import ReviewsFrom
from shop.models import ProductItem,Category,Reviews
from cart.models import CartItem,Order
from users.models import Profile


def Product_List(request):
    template = 'shop/shop-grid.html'
    products_lists = ProductItem.objects.select_related().all().order_by('-id')
    # qs_wish = ProductItem.objects.filter(quantity__lt=2)
    categories = Category.objects.all()
    filter = ProductFilter(request.GET, queryset=products_lists)

    context = {"product_lists": products_lists,
               "categories": categories,
               "filter": filter,
            #    'qs_wish': qs_wish,
               }
    return render(request, template, context)


def SizeView(request):
    template = 'shop/shop-grid.html'
    pass


def Categories_List(request, category_list,):
    categories = Category.objects.all()
    c = get_object_or_404(Category, slug=category_list,)
    products = c.productitem_set.all()
    page_title = c.name

    # set paginator
    page = request.GET.get('page', 1)  # get 1st page
    paginator = Paginator(products, 30)  # Only Show 10 review in per page
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # end paginator

    context = {
        "products": products,
        "categories": categories,
        "page_title": page_title,
    }
    return render(request, 'shop/singel_categories.html', context)


def product_details_and_review(request, product_slug):
    template = 'shop/shop-details.html'
    related_product = ProductItem.objects.select_related().all().order_by('-titel')

    if request.user.is_authenticated:
        user_pic = Profile.objects.get(user=request.user)
        
    product_details = get_object_or_404(ProductItem, slug=product_slug,)

    review = product_details.reviews_set.all()[:15]
    # this is the line to categorize comments
    # [:15] only 15 comments show in template
    # [node.get_descendants(include_self=True)for node in Reviews.objects.all() ]

    models = ProductItem.objects.get(slug=product_slug)
    if request.method == 'POST':
        model = Order.objects.get(user=request.user, ordered=False)
        model.shoes_size = request.POST.get('shoes_data')
        model.shirt_size = request.POST.get('shirt_data')
        model.pant_size = request.POST.get('pant_data')

        model.user = request.user
        model.save()

        messages.success(request, f"Success!!")
    else:
        pass

    user_review = None  # first Assign user_review none

    if request.method == "POST":
        form = ReviewsFrom(request.POST, request.FILES)
        if form.is_valid():
            user_review = form.save(commit=False) # not yet save in database
            # (product_item foreigkey) select Product item
            user_review.product_item = product_details
            user_review.user = request.user  # select user
            if user_pic != None:
                user_review.user_pic = user_pic  # select user profile_pic
            user_review.save()
            users = form.cleaned_data.get('user')
            return HttpResponseRedirect('.')
    else:
        form = ReviewsFrom()
    context = {
        'form': form,
        'review': review,
        'product_details': product_details,
        'user_review':  user_review,
        'related_product': related_product,
        'models' : models,
    }
    return render(request, template, context)


def ReviewList(request):
    template = 'shop/show_all_review.html'
    review = Reviews.objects.select_related().all()

    context = {
        'review': review,
    }
    return render(request, template, context)


def ReviewUpdate(request, id, **kwargs):
    template = 'shop/review_update_form.html'
    instance = get_object_or_404(Reviews, id=id)
    form = ReviewsFrom(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    context = {
        'form': form,
    }

    return render(request, template, context)


def ReviewDelete(request, id, **kwargs):
    template = 'shop/review_delete_form.html'
    instance = get_object_or_404(Reviews, id=id)
    # form = ReviewsFrom(request.POST or None, instance=instance)
    if request.method == 'POST':
        instance.delete()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    context = {
        'instance': instance,
    }

    return render(request, template, context)
