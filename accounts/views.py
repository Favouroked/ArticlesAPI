import jwt
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()

jwt_secret = 'THE_SECRET_OF_THE_UNIVERSE'


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_users(request):
    jwt_header = request.META.get('HTTP_AUTHORIZATION')
    if jwt_header is not None:
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No Authorization"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        data = {'id': user.id}
        payload = jwt.encode(data, jwt_secret, algorithm='HS256')
        return Response({'token': payload}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'error': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
