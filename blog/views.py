from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import blog.models as models
from auth_sys.models import MyUser



def index(request):
    return render(request, "blog/index.html", {"articles":models.Article.objects.all()})

def eror(request):
    if request.GET.get("eror_text") != None:
        return render(request, "eror.html", context={"eror_text":request.GET.get("eror_text")})
    else:
        return render(request, "eror.html", context={"eror_text":"А як ти надіслав запит без тексту?:)"})


def view_user_info(request, username):
    if not MyUser.objects.filter(username=username).exists():
        return redirect("/eror?eror_text=Користувача з таким юзернеймом не існує.")
    context = {"user_v":MyUser.objects.get(username=username)}
    context["articles_num"] = models.Article.objects.filter(author=context["user_v"]).count()
    context["subscriptions"] = models.Subscription.objects.filter(who=context["user_v"])
    if context["subscriptions"].count() == 0: context["subscriptions"] = 0
    if request.user.is_authenticated:
        context["is_sub"] = models.Subscription.objects.filter(who=request.user, on_whom=context["user_v"]).exists()
    
    return render(request, "blog/view_user_info.html", context)


def view_article(request, article_pk):
    if not models.Article.objects.filter(pk=article_pk).exists():
        return redirect("/eror?eror_text=Статті з таким pk не існує.")
    text_elements = list(models.TextArticleElement.objects.filter(article=article_pk))
    file_elements = list(models.FileArticleElement.objects.filter(article=article_pk))
    elements = sorted(text_elements+file_elements, key=lambda element: element.num)
    return render(request, "blog/view_article.html", context={"article":models.Article.objects.get(pk=article_pk),
                                        "elements":elements, "comments":models.Comment.objects.filter(article=article_pk)})

@login_required
def create_article(request):
    if request.method == "GET":
        return render(request, "blog/create_article.html",
                      {"categories":[choice.value for choice in models.Article.Categories]})
    elif request.method == "POST":
        article = models.Article.objects.create(author=request.user,
                                                name=request.POST.get("name"),
                                                category=request.POST.get("category"))
        article.save()
        start_element = models.TextArticleElement.objects.create(article=article, num=0, text="")
        start_element.save()

        return redirect(f"/redact_article/{article.pk}")

@login_required
def redact_article(request, article_pk):
    if not models.Article.objects.filter(pk=article_pk).exists():
        return redirect("/eror?eror_text=Статті з таким pk не існує.")
    article = models.Article.objects.get(pk=article_pk)
    if request.user != article.author:
        return redirect("/eror?eror_text=Ви не можете редагувати чужі статті.")
    
    if request.method == "GET":
        text_elements = list(models.TextArticleElement.objects.filter(article=article_pk))
        file_elements = list(models.FileArticleElement.objects.filter(article=article_pk))
        elements = sorted(text_elements+file_elements, key=lambda element: element.num)
        return render(request, "blog/redact_article.html",
            {"article":article, "elements":elements, "categories":[choice.value for choice in models.Article.Categories]})
    elif request.method == "POST":
        if request.GET.get("crud") == None: #Якщо це просто POST-запит, тобто користувач зберігає статтю
            for element_num in range(models.Article.objects.get(pk=article_pk).elements_num):
                if request.POST.get(str(element_num)) != None:
                    element = models.TextArticleElement.objects.get(article=article_pk, num=element_num)
                    element.text = request.POST.get(str(element_num))
                    element.save()
            return redirect("blog:index")
        elif request.GET.get("crud") == "create": #Якщо користувач додає новий елемент
            #Оновлюємо всі елементи
            must_update_num = []
            for element_num in range(article.elements_num):
                if request.POST.get(str(element_num)) != None:
                    element = models.TextArticleElement.objects.get(article=article_pk, num=element_num)
                    element.text = request.POST.get(str(element_num))
                    element.save()
                    if element_num > int(request.GET.get("num")):
                        must_update_num.append(element)
                elif element_num > int(request.GET.get("num")):
                    must_update_num.append(models.FileArticleElement.objects.get(article=article_pk, num=element_num))
            #Збільшуємо num у елементів, що йдуть після доданого елементу
            for element in must_update_num:
                element.num += 1
                element.save()
            #Додаємо новий елемент
            if request.GET.get("t") == "text":
                element = models.TextArticleElement(article=article, num=int(request.GET.get("num"))+1, text="")
                element.save()
            else:
                new_file = request.FILES.get("new_file")
                if new_file:
                    element = models.FileArticleElement(article=article, num=int(request.GET.get("num"))+1, file=new_file)
                    element.save()
                else:
                    element = models.TextArticleElement(article=article, num=int(request.GET.get("num"))+1,
                                                        text="Ви не додали файл, який потрібно додати")
                    element.save()

            #Оновлюємо elements_num у article
            article.elements_num += 1
            article.save()

            return redirect(f"/redact_article/{article.pk}")
        elif request.GET.get("crud") == "delete": #Якщо користувач видаляє існуючий елемент
            #Видаляємо елемент
            if request.GET.get("t") == "text":
                models.TextArticleElement.objects.get(article=article_pk, num=int(request.GET.get("num"))).delete()
            else:
                models.FileArticleElement.objects.get(article=article_pk, num=int(request.GET.get("num"))).delete()
            #Оновлюємо всі елементи до видаленого
            for element_num in range(int(request.GET.get("num"))):
                if request.POST.get(str(element_num)) != None:
                    element = models.TextArticleElement.objects.get(article=article_pk, num=element_num)
                    element.text = request.POST.get(str(element_num))
                    element.save()
            #Оновлюємо всі елемент після видаленого, також зменшуючи їйній num на 1
            for element_num in range(int(request.GET.get("num"))+1, article.elements_num):
                if request.POST.get(str(element_num)) != None:
                    element = models.TextArticleElement.objects.get(article=article_pk, num=element_num)
                    element.text = request.POST.get(str(element_num))
                    element.num -= 1
                    element.save()
                else:
                    element = models.FileArticleElement.objects.get(article=article_pk, num=element_num)
                    element.num -= 1
                    element.save()
            #Зменшуємо elements_num на один, бо зменшилась кількість елементів
            article.elements_num -= 1
            article.save()

            return redirect(f"/redact_article/{article.pk}")
        else:
            return redirect("/eror?eror_text=crud не правильний.")

@login_required
def delete_article(request, article_pk):
    if not models.Article.objects.filter(pk=article_pk).exists():
        return redirect("/eror?eror_text=Статті з таким pk не існує.")
    article = models.Article.objects.get(pk=article_pk)
    if request.user != article.author:
        return redirect("/eror?eror_text=Ви не можете видаляти чужі статті.")
    
    text_elements = list(models.TextArticleElement.objects.filter(article=article_pk))
    file_elements = list(models.FileArticleElement.objects.filter(article=article_pk))
    elements = sorted(text_elements+file_elements, key=lambda element: element.num)

    for element in elements: element.delete()
    article.delete()

    return redirect("blog:index")


@login_required
def add_comment(request, article_pk):
    if request.method == "POST":
        if not models.Article.objects.filter(pk=article_pk).exists():
            return redirect("/eror?eror_text=Статті з таким pk не існує.")
        comment = models.Comment.objects.create(author=request.user, article=models.Article.objects.get(pk=article_pk),
                                                text=request.POST.get("text"))
        comment.save()
        return redirect(f"/view_article/{article_pk}")
    else:
        return redirect("/eror?eror_text=Додати коментарій можна лише за допомогою POST запитів.")

@login_required
def delete_comment(request, article_pk, comment_pk):
    if not models.Article.objects.filter(pk=article_pk).exists():
        return redirect("/eror?eror_text=Статті з таким pk не існує.")
    if not models.Comment.objects.filter(pk=comment_pk).exists():
        return redirect("/eror?eror_text=Коментаря з таким pk не існує.")
    comment = models.Comment.objects.get(pk=comment_pk)
    if request.user != comment.author:
        return redirect("/eror?eror_text=Ви не можете видаляти чужі коментарі.")

    comment.delete()

    return redirect(f"/view_article/{article_pk}")


@login_required
def subscribe(request, user_pk):
    if not MyUser.objects.filter(pk=user_pk).exists():
        return redirect("/eror?eror_text=Користувача з таким pk не існує.")
    on_whom = models.MyUser.objects.get(pk=user_pk)
    subscription = models.Subscription.objects.create(who=request.user, on_whom=on_whom)
    subscription.save()

    return redirect(f"/view_user_info/{request.user.username}")

@login_required
def unsubscribe(request, user_pk):
    if not MyUser.objects.filter(pk=user_pk).exists():
        return redirect("/eror?eror_text=Користувача з таким pk не існує.")
    on_whom = models.MyUser.objects.get(pk=user_pk)
    subscription = models.Subscription.objects.get(who=request.user, on_whom=on_whom)

    subscription.delete()

    return redirect(f"/view_user_info/{request.user.username}")
