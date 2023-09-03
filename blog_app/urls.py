from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_f, name="login"),
    path("logout/", views.logout_f, name="logout"),
    path("post/list/", views.post_list, name="post_list"),
    path("post/search/", views.post_search, name="post_search"),
    path("post/detail/<str:pk>/", views.post_detail, name="post_detail"),
    path("post/create/", views.post_create, name="post_create"),
    # path("post/update/<str:pk>/", views.home, name="post_update"),
    # path("post/hide/<str:pk>/", views.post_hide, name="post_hide"),
    path("post/comment/create/<str:pk>/", views.post_comment_create, name="post_comment_create"),
    path("post/rating/<str:pk>/<str:is_like>/", views.post_rating, name="post_rating"),
    path("password/recover/", views.user_password_recover_send, name="user_password_recover_send"),
]