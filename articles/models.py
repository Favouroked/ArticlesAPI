from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    content = models.TextField()

    def __str__(self):
        return self.title
