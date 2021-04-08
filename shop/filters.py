from . models import *
import django_filters
from django import forms
from django_filters.filters import RangeFilter,DateFilter,CharFilter
from django_filters.widgets import RangeWidget,CSVWidget,DateRangeWidget,SuffixedMultiWidget
from django.forms import CheckboxSelectMultiple,RadioSelect


# Creating product filters
class ProductFilter(django_filters.FilterSet):
	titel = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'What Do You Need?'}), label=False)
	brand = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Whice Brand Do You Want?'}), label='Filter with brand')

	price = django_filters.RangeFilter()
	price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
	price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

	# colors = django_filters.filters.ChoiceFilter(choices=COLORS,widget=forms.Select(attrs={'class': 'custom-select form-control'},))
	# colors = django_filters.filters.ChoiceFilter(choices=COLORS,null_label='what is null',empty_label='select' ,widget= RadioSelect(attrs={'class': 'custom-select form-control '}))
	colors = django_filters.filters.ChoiceFilter(choices=COLORS,empty_label=None,widget= RadioSelect())

	class Meta:
		model = ProductItem
		fields = ['titel','price','colors',"date_added", 'brand']










































		# filter_overrides = {

		#  models.CharField: {      
		#      'filter_class': django_filters.CharFilter,
		#      'extra': lambda f: {
		#          'lookup_expr': 'icontains',
		#      },
		#  },

		#  models.BooleanField: {
		#      'filter_class': django_filters.DateFilter,
		#      'extra': lambda f: {
		#          'widget': forms.CheckboxInput,
		#      },
		#  },
		# }

# class RangeWidget(SuffixedMultiWidget):
# 	suffixes = ['min', 'max']


# 	def __init__(self, *args, **kwargs):
# 	   super(ProductFilter, self).__init__(*args, **kwargs)
# 	   self.filters['titel'].label="Article"
# 	   # self.filters['CompanySellerID'].label="Seller"
# 	   # self.filters['CompanyRegisterID'].label="Cash register"