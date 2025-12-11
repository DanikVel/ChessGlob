from django.urls import path
import blog.views as views


urlpatterns = [
    path("", views.index, name="index"),
    path("view_my_articles", views.view_my_articles, name="view_my_articles"),
    path("eror", views.eror, name="eror"),

    path("view_user_info/<str:username>", views.view_user_info, name="view_user_info"),

    path("view_article/<int:article_pk>", views.view_article, name="view_article"),
    path("create_article", views.create_article, name="create_article"),
    path("redact_article/<int:article_pk>", views.redact_article, name="redact_article"),
    path("delete_article/<int:article_pk>", views.delete_article, name="delete_article"),

    path("add_comment/<int:article_pk>", views.add_comment, name="add_comment"),
    path("delete_comment/<int:article_pk>/<int:comment_pk>", views.delete_comment, name="delete_comment"),

    path("like_article/<int:article_pk>", views.like_article, name="like_article"),
    path("unlike_article/<int:article_pk>", views.unlike_article, name="unlike_article"),
    path("dislike_article/<int:article_pk>", views.dislike_article, name="dislike_article"),
    path("undislike_article/<int:article_pk>", views.undislike_article, name="undislike_article"),

    path("subscribe/<int:user_pk>", views.subscribe, name="subscribe"),
    path("unsubscribe/<int:user_pk>", views.unsubscribe, name="unsubscribe"),
    
    path("api/user", views.MyUserListView.as_view(), name="api_user_list"),
    path("api/user/<int:pk>", views.MyUserDetailView.as_view(), name="api_user_detail")
    ]

app_name = "blog"
