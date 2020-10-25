import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from typing_extensions import runtime

from network.models import PostForm, User, Post, Like, Follower


def index(request):
    all_posts = (Post.objects
                        .all()
                        .annotate(like_count=Count('likes'))
                        .order_by('-timestamp')
                )

    likes_by_user = (Like.objects.filter(liker=request.user))
    liked_posts = Post.objects.filter(likes__in=likes_by_user)

    owned_posts = Post.objects.filter(owner=request.user)
        
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'all_posts': all_posts,
        'liked_posts': liked_posts,
        'owned_posts': owned_posts,
        'page_obj': page_obj,
        'page_number': page_number,
        'page_range': paginator.page_range
    }


    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                'form': PostForm,
                }
            return render(request, "network/new_post.html", context)

    else:
        context = {
            'form': PostForm,
        }

        return render(request, "network/new_post.html", context)


@login_required
def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(owner=user).order_by('-timestamp')

    followers = Follower.objects.filter(followed_by=user)
    following = Follower.objects.filter(following=user)

    context = {
        'profile_owner': user,
        'posts': posts,
        'followers': followers,
        'following': following,
    }

    return render(request, "network/user_profile.html", context)


@login_required
def follow_toggle(request, user_id):
    u = User.objects.get(pk=user_id)
    f = Follower.objects.filter(following=u,followed_by=request.user)
    if f.exists():
        f.delete()
    else:
        Follower.objects.create(
                            following=u,
                            followed_by=request.user
                        )
    return HttpResponseRedirect(reverse("user_profile"), kwargs={'user_id':request.user.id})


@login_required
def like_post(request):
    if request.method == "PUT":
        # Referenced from how project 3: mail handles json requests
        data = json.loads(request.body)

        post = Post.objects.filter(pk=data.get("id")).first()
        user = request.user

        like = Like.objects.filter(
                                post=post,
                                liker=user).first()
        if not like:
            Like.objects.create(
                        post=post,
                        liker=user,
            )
            return JsonResponse({
                            "like": "Post liked :)",
                            "id": data.get("id"),
                            "new_like": True
                        }, 
                        status=201)
        else:
            like.delete()
            return JsonResponse({
                            "like": "Post unliked",
                            "id": data.get("id"),
                            "new_like": False,                            
                        },
                        status=201)
    
    return JsonResponse({
            "error": "Invalid Request :("
        }, status=400)
