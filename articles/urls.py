from django.urls import path
from articles import views

urlpatterns = [
    path('submit/', views.submit_article, name='submit_article'),
    path('all/', views.all_articles, name='all_articles'),
    path('edit/', views.edit_article, name='edit_article'),
    path('delete/', views.delete_article, name='delete_article'),
    path('writer/<int:writer_id>/', views.individual_writer, name='individual_writer'),
]
