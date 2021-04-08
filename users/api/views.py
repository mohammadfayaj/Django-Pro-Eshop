from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.authentication import TokenAuthentication


from users.api.serializers import RegistrationsSerializer, MyTokenObtainPairSerializer




class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# @api_view(['POST',])
# @permission_classes([IsAuthenticated])
# def login_response(request):
# 	if request.method == "POST":
# 		serializers = LoginSerializer(data=request.data)
# 		data = {}
# 		if serializers.is_valid():
# 			user = serializers.save()
# 			data['response'] = ['successfully login']
# 			data['username'] = user.usernmae
# 		else:
# 			data = serializers.errors
# 	return Response(data)


@api_view(['POST',])
def registration_view(request):
	if request.method == 'POST':
		serializers = RegistrationsSerializer(data=request.data)
		data = {}
		if serializers.is_valid():
			user = serializers.save()
			data['response'] = ['successfully registered a new user.']
			data['email'] = user.email
			data['username'] = user.username
			token = Token.objects.get(user=user).key
			data['token'] = token
		else:
			data =serializers.errors
		return Response (data)
