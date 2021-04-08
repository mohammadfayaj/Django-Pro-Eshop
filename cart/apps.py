from django.apps import AppConfig

class CartConfig(AppConfig):
	name = 'cart'
	verbose_name = 'Customer Order Process'

	def ready(self):
		import cart.signals