from django import template
from shop.models import ProductItem

register = template.Library()

# hit in singel_categories.html
@register.filter
def count_total_product_item(count):
	count = ProductItem.objects.all()
	return count.count()
















