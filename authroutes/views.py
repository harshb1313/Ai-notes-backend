from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'status':200, 'message':'User Registered Successfully', 'user':{
            'username': user.username,
            'accesstoken': str(refresh.access_token),
            'refresh': str(refresh)
        }})
    return Response({'status':400, 'message':'User Registration Failed', 'errors': serializer.errors})