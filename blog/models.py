from django.db import models
from auth_sys.models import MyUser


#-----------------------------Моделі статтей
class Article(models.Model):
    class Categories(models.TextChoices):
        other = "Інше"
        debut = "Дебют"
        middle_game = "Мітельшпіль"
        end_game = "Ендшпіль"
        history = "Історія"
        etude = "Шахові задачки"
    author = models.ForeignKey(MyUser, models.CASCADE)
    name = models.CharField(max_length=32)
    category = models.CharField(choices=Categories.choices, default=Categories.other)
    created_time = models.DateTimeField()
    elements_num = models.IntegerField(default=1)

    def __str__(self): return f"{self.author.username}: {self.name} - {self.category}"

class TextArticleElement(models.Model):
    article = models.ForeignKey(Article, models.CASCADE)
    num = models.IntegerField()
    t = "text" #t - type. Потрібно, щоб відрізняти TextArticleElement від FileArticleElement
    text = models.TextField()
    
    def __str__(self): return f"{self.article.name} - {self.num}"

class FileArticleElement(models.Model):
    article = models.ForeignKey(Article, models.CASCADE)
    num = models.IntegerField()
    t = "file" #t - type. Потрібно, щоб відрізняти TextArticleElement від FileArticleElement
    file = models.FileField(upload_to="articles_media")

    def __str__(self): return f"{self.article.name} - {self.num}"

#-----------------------------Модель коментарів до статей
class Comment(models.Model):
    author = models.ForeignKey(MyUser, models.CASCADE)
    article = models.ForeignKey(Article, models.CASCADE)
    text = models.CharField()

    def __str__(self): return f"{self.author.username} - {self.article.name}"

#-----------------------------Модель лайку/дізлайку до статей
class Like(models.Model):
    article = models.ForeignKey(Article, models.CASCADE, related_name="like")
    author = models.ForeignKey(MyUser, models.CASCADE)

class Dislike(models.Model):
    article = models.ForeignKey(Article, models.CASCADE, related_name="dislike")
    author = models.ForeignKey(MyUser, models.CASCADE)

#-----------------------------Модель підписок користувачів
class Subscription(models.Model): #Підписка користувача, на іншого користувача, щоб отримувати інформацію про його статті
    who = models.ForeignKey(MyUser, models.CASCADE, related_name="subscription_who")
    on_whom = models.ForeignKey(MyUser, models.CASCADE, related_name="subscription_on_whom")
    email_newsletter = models.BooleanField(default=False)
