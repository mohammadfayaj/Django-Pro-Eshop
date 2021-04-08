from django.contrib import admin
from .models import *

class MyAdmin(admin.ModelAdmin):
	fields=['titel', 'header_image']
	def has_add_permission(self, request):
		if HeaderImage.objects.none():
			return True
		else:
			return True

admin.site.register(HeaderImage,MyAdmin)
admin.site.register(BannerImage)
admin.site.register(BlogPost)
admin.site.register(Contact)



