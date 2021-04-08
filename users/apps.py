from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Customer Information'

    def ready(self):
    	import users.signals
