from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import FollowUser, Profile, Post, LikePost


@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user__in=request.user.profile.followings)
    suggestions = (
        Profile.objects.all()
        .exclude(user__in=request.user.profile.followings)
        .exclude(id=request.user.profile.id)
        .order_by("?")[:4]
    )
    context = {"profile": profile, "posts": posts, "suggestions": suggestions}
    return render(request, "index.html", context)


@login_required
def follow(request, id):
    next = request.GET.get("next", None)
    follower = request.user
    user = User.objects.get(id=id)
    if user != follower:
        if FollowUser.objects.filter(user=user, follower=follower).exists():
            FollowUser.objects.get(user=user, follower=follower).delete()
        else:
            FollowUser.objects.create(user=user, follower=follower)

    return redirect(next if next else "index")


@login_required
def like_post(request, id):
    next = request.GET.get("next", None)
    user = request.user
    post = Post.objects.get(id=id)
    if LikePost.objects.filter(user=user, post=post).exists():
        LikePost.objects.get(user=user, post=post).delete()
        post.no_of_likes = F("no_of_likes") - 1
        post.save()
    else:
        LikePost.objects.create(user=user, post=post)
        post.no_of_likes = F("no_of_likes") + 1
        post.save()
    return redirect(next if next else "index")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required
def profile(request, username=None):
    if username:
        profile = Profile.objects.get(user__username__iexact=username)
    else:
        profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=profile.user)
    posts_length = len(posts)

    context = {"profile": profile, "posts": posts, "posts_length": posts_length}
    return render(request, "profile.html", context)


@login_required
def search(request):
    username = request.GET.get("username")
    profiles = Profile.objects.filter(user__username__icontains=username)
    print(profiles)
    return render(
        request,
        "index.html",
        {"page": "Search", "profiles": profiles, "username": username},
    )


@login_required
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        image = request.FILES.get("image", None)
        bio = request.POST.get("bio", None)
        location = request.POST.get("location", None)

        profile.profileimg = image if image else profile.profileimg
        profile.bio = bio if bio else profile.bio
        profile.location = location if location else profile.location
        profile.save()

    return render(request, "setting.html", {"profile": profile})


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Incorrect credentials passed!")
            return redirect("signin")

    return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password != password2:
            messages.error(request, "Password do not match")
            return redirect("signup")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")
        else:
            user = User.objects.create(
                username=username, email=email, password=password
            )
            Profile.objects.create(user=user, id_user=user.id)
            auth.login(request, user)
            return redirect("settings")

    return render(request, "signup.html")


@login_required
def upload(request):
    if request.method == "POST":
        image = request.FILES.get("image", None)
        caption = request.POST.get("caption", None)
        if not image and not caption:
            messages.error(request, "Both fields cant be empty")
            return redirect("index")
        post = Post.objects.create(user=request.user, image=image, caption=caption)
        post.save()
        return redirect("index")
    return redirect("index")
