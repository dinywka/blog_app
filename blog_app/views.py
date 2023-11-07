import datetime
import random
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from blog_app import models
from django.core.cache import caches, CacheHandler
from django.shortcuts import get_object_or_404


RamCache = caches["default"]
DatabaseCache = caches["extra"]



# Create your views here.
def home(request):
    return render(request, 'blog_app/home.html')

def about(request):
    return render(request, 'blog_app/about.html')

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
        return render(request, "blog_app/home.html")
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
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(posts, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(request, "blog_app/list.html", context={"current_page": current_page})


def post_detail(request: HttpRequest, pk: str) -> HttpResponse:
    """_view"""
    post = RamCache.get(f"post_detail_{pk}")
    if post is None:
        post = models.Post.objects.get(id=pk)  # тяжёлое обращение к базе данных -- 100x - 1000x
        RamCache.set(f"post_detail_{pk}", post, timeout=30)

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
        image = request.FILES.get("image", None)
        models.Post.objects.create(author=request.user, title=title, description=description, image=image if image else None)
        return redirect(reverse("post_list"))
    else:
        raise ValueError("Invalid method")


def post_delete(request, pk):
    if request.method != "GET":
        raise ValueError("Invalid method")

    post = models.Post.objects.get(id=int(pk))

    if post.author != request.user:
        raise PermissionDenied("You are not the author of this post.")

    post.delete()
    return redirect(reverse("post_list"))


def post_update(request, pk: str):
    """Обновление существующего мема."""

    post = get_object_or_404(models.Post, id=int(pk))
    if post.author != request.user:
        raise PermissionDenied("You are not the author of this post.")
    else:
        if request.method == "GET":
            return render(request, "blog_app/post_update.html", {'post': post})

        elif request.method == "POST":
            post.title = request.POST.get("title", post.title)  # Set title if present, else retain the old one
            post.description = request.POST.get("description", post.description)  # Similar for description

            if "image" in request.FILES:
                post.image = request.FILES["image"]

            post.save()
            return redirect(reverse("post_list"))

        else:
            raise ValueError("Invalid method")

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

#
# def user_password_recover_send(request):
#     if request.method == "GET":
#         context = {}
#         return render(request, "blog_app/user_password_recover_send.html", context)
#     elif request.method == "POST":
#         email = str(request.POST["email"]).strip()
#         users = User.objects.filter(username=email)
#         if len(users) < 1:
#             context = {"error": "Неправильное имя пользователя/почта", "email": email}
#             return render(request, "blog_app/user_password_recover_send.html", context)
#
#         try:
#             m_from = settings.EMAIL_HOST_USER
#             m_to = [email]
#             m_subject = "Восстановление доступа к аккаунту"
#             token = models.UserAuthToken.objects.create(user=users[0], token=models.UserAuthToken.token_generator())
#             # Yandex блокирует как спам, {} чтобы не блокировал. Письмо падает в Спам
#             token_key = {token.token}
#             m_message = f"Перейдите по ссылке: 'http://127.0.0.1:8000/user/password_recover/input/{token_key}/'"
#             print(m_message)
#             send_mail(m_subject, m_message, m_from, m_to)
#
#             context = {"success": "На указанную почту отправлен код восстанвления! Следуйте инструкциям в письме."}
#             return render(request, "blog_app/user_password_recover_send.html", context)
#         except Exception as error:
#             print(error)
#             return render(
#                 request,
#                 "blog_app/user_password_recover_send.html",
#                 {"error": str(error)},
#             )
#
# def user_password_recover_input(request: HttpRequest, token: str) -> HttpResponse:
#     try:
#         token = models.UserAuthToken.objects.get(token=str(token))
#         login(request, token.user)
#         token.delete()
#         return redirect(reverse("home"))
#     except Exception as error:
#         print(error)
#         return redirect(reverse("login"))
#
# def profile(request):
#     return render(request, "blog_app/profile.html")