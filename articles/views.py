import jwt
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.views import jwt_secret
from .models import Article
from .serializers import ArticleSerializer

# Create your views here.

User = get_user_model()


@api_view(['POST'])
def submit_article(request):
    jwt_header = request.META.get('HTTP_AUTHORIZATION')
    if jwt_header is not None:
        jwt_code = jwt_header.split(' ')[1]
        payload = jwt.decode(jwt_code, jwt_secret, algorithms=['HS256'])
        user_id = payload.get('id')
        authorized_user = User.objects.get(id=user_id)
        Article.objects.create(title=request.data.get('title'), content=request.data.get('content'),
                               user=authorized_user)
        return Response({"created": True}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "No Authorization"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_article(request):
    jwt_header = request.META.get('HTTP_AUTHORIZATION')
    if jwt_header is not None:
        jwt_code = jwt_header.split(' ')[1]
        payload = jwt.decode(jwt_code, jwt_secret, algorithms=['HS256'])
        user_id = payload.get('id')
        article = Article.objects.get(id=request.data.get('id'))
        if user_id == article.user.id:
            article.title = request.data.get('title') or article.title
            article.content = request.data.get('content') or article.content
            article.save()
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not authorized to edit"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error": "No Authorization"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_article(request):
    jwt_header = request.META.get('HTTP_AUTHORIZATION')
    if jwt_header is not None:
        jwt_code = jwt_header.split(' ')[1]
        payload = jwt.decode(jwt_code, jwt_secret, algorithms=['HS256'])
        user_id = payload.get('id')
        article = Article.objects.get(id=request.data.get('id'))
        if user_id == article.user.id:
            article.delete()
            return Response({"message": "It has been deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not authorized to delete"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error": "No Authorization"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_articles(request):
    jwt_header = request.META.get('HTTP_AUTHORIZATION')
    if jwt_header is not None:
        serializer = ArticleSerializer(Article.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No Authorization"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def individual_writer(request, writer_id):
    jwt_header = request.META.get('HTTP_AUTHORIZATION')
    if jwt_header is not None:
        serializer = ArticleSerializer(Article.objects.filter(user_id=writer_id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No Authorization"}, status=status.HTTP_400_BAD_REQUEST)
