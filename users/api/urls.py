from django.urls import path
from users.api import views
from rest_framework_simplejwt.views import TokenRefreshView
from users.api.views import MyObtainTokenPairView

urlpatterns = [

    path('registration/', views.registration_view),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh')



]