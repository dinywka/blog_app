from django.shortcuts import render

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
import re
from blog_app import models


# Create your views here.
def home(request):
    return render(request, 'blog_app/home.html')

def register(request):
    if request.method == "GET":
        return render(request, "blog_app/register.html")
    elif request.method == "POST":
        email = request.POST.get("email", None)  # Admin1@gmail.com
        password = request.POST.get("password", None)  # Admin1@gmail.com
        if (
                re.match(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", email) is None
        ):
            return render(
                request,
                "blog_app/register.html",
                {"error": "Некорректный формат email или пароль"},
            )
        try:
            User.objects.create(
                username=email,
                password=make_password(password),
                email=email,
            )
        except Exception as error:
            return render(
                request,
                "blog_app/register.html",
                {"error": str(error)},
            )
        return render(request, "blog_app/list.html")
    else:
        raise ValueError("Invalid method")


def login_f(request: HttpRequest) -> HttpResponse:
    """Вход в аккаунт пользователя."""

    if request.method == "GET":
        return render(request, "blog_app/login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is None:
            return render(request, "blog_app/login.html", {"error": "Некорректный email или пароль"})
        login(request, user)
        return redirect(reverse("home"))
    else:
        raise ValueError("Invalid method")


def logout_f(request: HttpRequest) -> HttpResponse:
    """Выход из аккаунта"""
    logout(request)
    return redirect(reverse('login'))


def post_list(request: HttpRequest) -> HttpResponse:
    """_view"""

    posts = models.Post.objects.all()

    return render(request, "blog_app/list.html", {"posts": posts})
#
#
# def post_detail(request: HttpRequest, pk: str) -> HttpResponse:
#     """_view"""
#     return redirect(reverse("login"))
#
#
# # def create_view(request: HttpRequest, pk: str) -> HttpResponse:
# #     """_view"""
# #     return redirect(reverse("login"))
#
#
def post_create(request):
    """Создание нового мема."""

    if request.method == "GET":
        return render(request, "blog_app/create_post.html")
    elif request.method == "POST":
        title = request.POST.get("title", None)
        description = request.POST.get("description", None)
        image = request.FILES["image"]
        models.Post.objects.create(author=request.user, title=title, description=description, image=image)  # SQL
        return redirect(reverse("post_list"))
    else:
        raise ValueError("Invalid method")
#
#
#
# def post_update(request, pk: str):
#     """Обновление существующего мема."""
#
#     if request.method == "GET":
#         mem = models.Mem.objects.get(id=int(pk))  # SQL
#         mem.title = mem.title[::-1]
#         # mem.is_moderate = False
#         mem.save()
#         return redirect(reverse("list"))
#     else:
#         raise ValueError("Invalid method")
#
#
# def post_delete(request, pk: str):
#     """Удаление мема."""
#
#     if request.method == "GET":
#         mem = models.Mem.objects.get(id=int(pk))  # SQL
#         mem.delete()
#         return redirect(reverse("list"))
#     else:
#         raise ValueError("Invalid method")
#
#
# def tags(request):
#     memes = [
#         {
#             "id": x,
#             "title": f"Наименование {x}",
#             "description": {"data1": {"price": random.randint(1, 1000000) + random.random()}}
#
#         }
#         for x in range(1, 20 + 1)
#     ]
#     return render(request, "blog_app/tags.html", {"memes": memes})
#
#
#
# def news_comments_create(request, pk):
#     """Создание комментария."""
#
#     if request.method != "POST":
#         raise Exception("Invalid method")
#
#     news = models.News.objects.get(id=int(pk))
#     user = request.user
#     text = request.POST.get("text", "")
#     models.NewsComments.objects.create(news=news, author=user, text=text)
#
#     return redirect(reverse('news_detail', args=(pk,)))
#
#
# def rating_change(request, pk, status):
#     """Создаёт рейтинг к новости"""
#
#     if request.method == "GET":
#         post_obj = models.News.objects.get(id=int(pk))
#         author_obj = request.user
#         status = True if int(status) == 1 else False
#         post_rating_objs = models.NewsRatings.objects.filter(post=post_obj, author=author_obj)
#         if len(post_rating_objs) <= 0:
#             models.NewsRatings.objects.create(post=post_obj, author=author_obj, status=status)
#         else:
#             post_rating_obj = post_rating_objs[0]
#             if (status is True and post_rating_obj.status is True) or \
#                     (status is False and post_rating_obj.status is False):
#                 post_rating_obj.delete()
#             else:
#                 post_rating_obj.status = status
#                 post_rating_obj.save()
#         return redirect(reverse('news_detail', args=[pk]))
#     else:
#         raise Exception("Method not allowed!")
#
#
#
#
#
