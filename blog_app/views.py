import datetime
import random
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from blog_app import models
from django.core.cache import caches, CacheHandler

RamCache = caches["default"]
DatabaseCache = caches["extra"]



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


def post_detail(request: HttpRequest, pk: str) -> HttpResponse:
    """_view"""
    post = RamCache.get(f"post_detail_{pk}")
    if post is None:
        post = models.Post.objects.get(id=pk)  # тяжёлое обращение к базе данных -- 100x - 1000x
        RamCache.set(f"post_detail_{pk}", post, timeout=30)

    # Если мы поставили лайк - то закрашиваем кнопку
    # post + user

    comments = models.PostComments.objects.filter(post=post)
    ratings = models.PostRatings.objects.filter(post=post)
    ratings = {
        "like": ratings.filter(status=True).count(),
        "dislike": ratings.filter(status=False).count(),
        "total": ratings.filter(status=True).count() - ratings.filter(status=False).count(),
    }

    return render(request, "blog_app/post_detail.html",
                  context={"post": post, "comments": comments, "ratings": ratings, "is_detail_view": True})



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

@login_required
def post_search(request: HttpRequest) -> HttpResponse:
    search = str(request.POST.get("search", ""))
    posts = models.Post.objects.filter(is_active=True, title__icontains=search)
    return render(request, "blog_app/post_search.html", {"posts": posts, "search": search})
def post_comment_create(request: HttpRequest, pk: str) -> HttpResponse:
    """Создание комментария."""

    post = models.Post.objects.get(id=int(pk))
    text = request.POST.get("text", "")
    models.PostComments.objects.create(post=post, author=request.user, text=text)

    return redirect(reverse("post_detail", args=(pk,)))

def post_rating(request: HttpRequest, pk: str, is_like: str) -> HttpResponse:
    post = models.Post.objects.get(id=int(pk))
    is_like = True if str(is_like).lower().strip() == "лайк" else False  # тернарный оператор

    ratings = models.PostRatings.objects.filter(post=post, author=request.user)
    if len(ratings) < 1:
        models.PostRatings.objects.create(post=post, author=request.user, status=is_like)
    else:
        rating = ratings[0]
        if is_like == True and rating.status == True:
            rating.delete()
        elif is_like == False and rating.status == False:
            rating.delete()
        else:
            rating.status = is_like
            rating.save()

    return redirect(reverse("post_detail", args=(pk,)))


def user_password_recover_send(request):
    if request.method == "GET":
        context = {}
        return render(request, "blog_app/user_password_recover_send.html", context)
    elif request.method == "POST":
        email = str(request.POST["email"]).strip()
        users = User.objects.filter(username=email)
        if len(users) < 1:
            context = {"error": "Неправильное имя пользователя/почта", "email": email}
            return render(request, "blog_app/user_password_recover_send.html", context)

        """
        ОТПРАВКА ПИСЬМА это платно*, поэтому нужно будет потом придумать как ограничить


        1. SendPulse - 
        + гибко, есть html шаблоны, не блочится другими почтами...
        - платно, сложное api

        2. Яндекс smtp
        2.1 Создать яндекс аккаунт
        2.2 Зайти в настройки (https://id.yandex.kz/security/app-passwords) - пароль от SMTP сохранить
        2.3 Создать и настроить ENV-файл(переменные окружения)
        2.4 В Django задать переменные (EMAIL_HOST...)
        2.5 Отправить письмо через send_mail(...)
        + бесплатно, не блочится другими почтами
        - есть ограничения

        """
        try:
            m_from = settings.EMAIL_HOST_USER
            m_to = [email]
            m_subject = "Восстановление доступа к аккаунту"
            m_message = f"Ваш старый пароль: {users[0].password} {datetime.datetime.now()}"  # TODO
            # TODO HTML
            send_mail(m_subject, m_message, m_from, m_to)

            context = {"success": "На указанную почту отправлен код восстанвления! Следуйте инструкциям в письме."}
            return render(request, "blog_app/user_password_recover_send.html", context)
        except Exception as error:
            print(error)
            return render(
                request,
                "blog_app/user_password_recover_send.html",
                {"error": str(error)},
            )