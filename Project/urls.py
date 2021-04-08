"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import notifications.urls
import star_ratings.urls
# import debug_toolbar
from django.views.generic import RedirectView, TemplateView

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    path('', include('blog.urls', namespace='blog')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('users/', include('users.urls', namespace='users')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('', include('social_django.urls', namespace='social')),
    
    path('admin/', admin.site.urls),

    # path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    # path('__debug__/', include(debug_toolbar.urls)),

    #rest_framework_url
    path('api-auth/', include('rest_framework.urls')),
    path('api-login/', obtain_auth_token),
    
    path('api/blog/', include('blog.api.urls')),
    path('api/cart/', include('cart.api.urls')),
    path('api/shop/', include('shop.api.urls')),
    path('api/users/', include('users.api.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
