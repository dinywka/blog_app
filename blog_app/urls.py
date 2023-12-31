from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.login_f, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_f, name="logout"),
    path("post/list/", views.post_list, name="post_list"),
    path("post/search/", views.post_search, name="post_search"),
    path("post/detail/<str:pk>/", views.post_detail, name="post_detail"),
    path("post/create/", views.post_create, name="post_create"),
    path("post/delete/<str:pk>/", views.post_delete, name="post_delete"),
    path("post/update/<str:pk>/", views.post_update, name="post_update"),
    path("post/comment/create/<str:pk>/", views.post_comment_create, name="post_comment_create"),
    path("post/rating/<str:pk>/<str:is_like>/", views.post_rating, name="post_rating"),
    # path("password/recover/", views.user_password_recover_send, name="user_password_recover_send"),
    # path("user/password_recover/login/", views.user_password_recover_send, name="user_password_recover_login"),
    # path("user/password_recover/input/<str:token>/", views.user_password_recover_input, name="user_password_recover_input"),
]