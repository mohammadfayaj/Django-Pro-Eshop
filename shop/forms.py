from django import forms
from .models import *
from django.shortcuts import render, get_object_or_404
from mptt.forms import TreeNodeChoiceField


class ReviewsFrom(forms.ModelForm):

	parent = TreeNodeChoiceField(queryset=Reviews.objects.select_related().all())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['parent'].widget.attrs.update(
		    {'class': 'd-none'})
		self.fields['parent'].label = ''
		self.fields['parent'].required = False

	class Meta:
		model = Reviews
		# fields = '__all__'
		fields = ['review','parent', 'image']
		widgets = {
		    'review': forms.TextInput(attrs={'class': 'col-sm-12'}),
		}

	def save(self, *args, **kwargs):
		Reviews.objects.rebuild()
		return super(ReviewsFrom, self).save(*args, **kwargs)
