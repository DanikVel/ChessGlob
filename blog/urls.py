from django.urls import path
import blog.views as views


urlpatterns = [
    path("", views.index, name="index"),
    path("view_article/<int:article_pk>", views.view_article, name="view_article"),
    path("create_article", views.create_article, name="create_article"),
    path("redact_article/<int:article_pk>", views.redact_article, name="redact_article"),
    path("delete_article/<int:article_pk>", views.delete_article, name="delete_article"),
    path("add_comment/<int:article_pk>", views.add_comment, name="add_comment"),
    path("delete_comment/<int:article_pk>/<int:comment_pk>", views.delete_comment, name="delete_comment")
    ]

app_name = "blog"
