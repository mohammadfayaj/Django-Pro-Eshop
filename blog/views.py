from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from shop.models import ProductItem,Category
from django.core.exceptions import ObjectDoesNotExist
from .models import HeaderImage,BannerImage,BlogPost,Contact
from shop.filters import ProductFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.authtoken.models import Token
from django.contrib import messages

def Product_List(request):
	template = 'blog/home.html'

	products_lists = ProductItem.objects.select_related().all()
	filter = ProductFilter(request.GET, queryset= products_lists)
	header_image = HeaderImage.objects.all()
	banner = BannerImage.objects.all()
	blog = BlogPost.objects.select_related().all() 

    # Paginator ------
	paginator = Paginator(products_lists, 30)
	page_number = request.GET.get('page', 1)
	try:
		products_lists = paginator.page(page_number)
	except PageNotAnInteger:
		products_lists = paginator.page(1)
	except EmptyPage:
		products_lists = paginator.page(paginator.num_pages)
	finally:
		pass

	context = {"products_lists" : products_lists, 
	           "filter" : filter, 
	           "header_image" : header_image,
	           "banner" : banner,
	           "blog" : blog,

	           }
	return render(request, template, context)


def Product_Details(request,product_slug):
    template = 'shop/shop-details.html'
    product_details = ProductItem.objects.get(slug=product_slug)
    context = {'product_details': product_details}
    return render(request, template, context)


def Categories_List(request, category_list,):
	categories = Category.objects.select_related('parent').all()
	c = get_object_or_404(Category, slug = category_list,)
	products = c.productitem_set.all()
	page_title = c.name 
	context = {
	    "products" : products,
	    "categories" : categories, 
	    "page_title" : page_title,
	}
	return render(request, 'shop/singel_categories.html', context)


def blog (request):
	template = "blog/blog.html"
	blog = BlogPost.objects.select_related('users').all()
	return render (request, template ,{ 'blog' : blog })


def blog_details (request, id):
	template = "blog/blog-details.html"
	qs_blog = get_object_or_404(BlogPost, id=id)

	return render (request, template ,{ 'qs_blog' : qs_blog })


def shop_contact(request):
	template = "base/contact.html"
	contact = Contact.objects.all()
	context = {'contact': contact}
	return render(request, template, context )


def api_view(request):
	template = 'api/api_home.html'
	if request.user.is_authenticated:
		try:
			token = Token.objects.get(user=request.user).key
			context = {'token': token}
			return render(request, template, context )
		except ObjectDoesNotExist:
			empty_massage = "You Don't Have API TOKEN"
			context = {'empty_massage': empty_massage,}
			return render(request, template, context )
	else:
		return render(request, template,)

	return render(request, template,)