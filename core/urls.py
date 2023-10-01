from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("follow/<int:id>/", views.follow, name="follow"),
    path("like-post/<uuid:id>/", views.like_post, name="like-post"),
    path("logout", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("search/", views.search, name="search"),
    path("settings/", views.settings, name="settings"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("upload/", views.upload, name="upload"),
]
