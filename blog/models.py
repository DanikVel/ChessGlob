from django.db import models
from auth_sys.models import MyUser


class Article(models.Model):
    class Categories(models.TextChoices):
        debut = "Дебют"
        middle_game = "Мітельшпіль"
        end_game = "Ендшпіль"
        history = "Історія"
        etude = "Шахові задачки"
        other = "Інше"
    author = models.ForeignKey(MyUser, models.CASCADE)
    name = models.CharField(max_length=32)
    category = models.CharField(choices=Categories.choices, default=Categories.other)

    def __str__(self): return f"{self.author}: {self.name} - {self.category}"

class TextArticleElement(models.Model):
    article = models.ForeignKey(Article, models.CASCADE)
    num = models.IntegerField()
    text = models.TextField()
    
    def __str__(self): return f"{self.article.name}"

class FileArticleElement(models.Model):
    article = models.ForeignKey(Article, models.CASCADE)
    num = models.IntegerField()
    file = models.FileField(upload_to="articles_media")

    def __str__(self): return f"{self.article.name}"
