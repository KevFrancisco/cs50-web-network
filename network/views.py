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
    # Get all Posts
    all_posts = (
        Post.objects.all().annotate(like_count=Count("likes")).order_by("-timestamp")
    )

    # Explicitly declare to None, this hides all the [edit buttons] and [active like]
    # indicators in the index view if the user is AnonUser (aka unauthenticated user)
    liked_posts = None
    owned_posts = None

    # If the user is authenticated, we shadw the context with a list of their likes
    # and which posts they own, then we filter the template like so:
    # if [posts] in [owned_posts] then show edit button
    if request.user.is_authenticated:
        likes_by_user = Like.objects.filter(liker=request.user)
        liked_posts = Post.objects.filter(likes__in=likes_by_user)
        owned_posts = Post.objects.filter(owner=request.user)

    # Paginator, show ten (10) posts only per viewing, taken from django docs example
    # https://docs.djangoproject.com/en/3.1/topics/pagination/
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Pass the contexts neatly :D
    context = {
        "form": PostForm,
        "all_posts": all_posts,
        "liked_posts": liked_posts,
        "owned_posts": owned_posts,
        "page_obj": page_obj,
        "page_number": page_number,
        "page_range": paginator.page_range,
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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, first_name=firstname, last_name=lastname
            )
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
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
                "form": PostForm,
            }
            return render(request, "network/new_post.html", context)

    else:
        context = {
            "form": PostForm,
        }

        return render(request, "network/new_post.html", context)


@login_required
def user_profile(request, profile_user_id):
    # Get the user requested in the url and their posts
    profile_user = User.objects.get(pk=profile_user_id)
    posts = (
        Post.objects.filter(owner=profile_user)
        .annotate(like_count=Count("likes"))
        .order_by("-timestamp")
    )

    # Since the template uses these contexts by default, we also need to import this
    # Refactor to minimize db querying
    # Maybe we can remove this if the request is for a user profile and we can filter inline
    likes_by_user = Like.objects.filter(liker=request.user)
    liked_posts = Post.objects.filter(likes__in=likes_by_user)
    owned_posts = Post.objects.filter(owner=request.user)

    # Paginator... Requirment was 10 posts per page
    # Bet I can make an infinite scrolling version ala pinterest :P
    # Personally, in don't like pagination from a usability standpoint... :/
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get Follower + Following counts and list em out for easy access
    following = Follower.objects.filter(followed_by=profile_user)
    followers = Follower.objects.filter(following=profile_user)
    # Get a qset of users that follow the profile owner for templating
    user_followers = User.objects.filter(followed_by__in=followers)

    context = {
        "profile_owner": profile_user,
        "all_posts": posts,
        "liked_posts": liked_posts,
        "owned_posts": owned_posts,
        "page_obj": page_obj,
        "page_number": page_number,
        "page_range": paginator.page_range,
        "followers": followers,
        "following": following,
        "user_followers": user_followers,
    }

    return render(request, "network/user_profile.html", context)


@login_required
def follow_toggle(request):
    if request.method == "PUT":
        # Get the JSON data
        data = json.loads(request.body)
        to_follow_id = data.get("to_follow_id")

        # The user object to follow
        u_to_follow = User.objects.filter(pk=to_follow_id).first()
        f = Follower.objects.filter(
            following=u_to_follow, followed_by=request.user
        ).first()

        # Check if the follow already exists or not
        if f:
            f.delete()
            return JsonResponse(
                {
                    "Status": "Success! User Unfollowed",
                    "u_to_follow": u_to_follow.username,
                    "new_follow": False,
                },
                status=200,
            )
        else:
            Follower.objects.create(following=u_to_follow, followed_by=request.user)
            return JsonResponse(
                {
                    "Status": "Success! User Followed",
                    "u_to_follow": u_to_follow.username,
                    "new_follow": True,
                },
                status=201,
            )

    # Only accept PUT requests
    return JsonResponse({"error": "Invalid Request :("}, status=400)


@login_required
def like_post(request):
    if request.method == "PUT":
        # Referenced from how project 3: mail handles json requests
        data = json.loads(request.body)

        post = Post.objects.filter(pk=data.get("id")).first()
        user = request.user

        like = Like.objects.filter(post=post, liker=user).first()
        if not like:
            Like.objects.create(
                post=post,
                liker=user,
            )
            return JsonResponse(
                {"like": "Post liked :)", "id": data.get("id"), "new_like": True},
                status=201,
            )
        else:
            like.delete()
            return JsonResponse(
                {
                    "like": "Post unliked",
                    "id": data.get("id"),
                    "new_like": False,
                },
                status=201,
            )

    return JsonResponse({"error": "Invalid Request :("}, status=400)


@login_required
def edit_post(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        post = Post.objects.filter(pk=data.get("id")).first()
        new_content = data.get("text")

        if post.owner != request.user:
            return JsonResponse(
                {
                    "error": "Forbidden, Only the post owner may edit a post",
                    "owner": post.owner.id,
                },
                status=403,
            )

        if post:
            post.text = new_content
            post.save()
            return JsonResponse(
                {
                    "edit": "Post edited :)",
                    "new_content": new_content,
                },
                status=201,
            )
        else:
            return JsonResponse({"error": "Invalid Post"}, status=400)

    return JsonResponse({"error": "Invalid Request"}, status=400)


@login_required
def delete_post(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        post = Post.objects.filter(pk=data.get("id")).first()

        if post.owner != request.user:
            return JsonResponse(
                {
                    "error": "Forbidden, Only the owner may edit a post",
                    "owner": post.owner.id,
                },
                status=403,
            )

        if post:
            post.delete()
            return JsonResponse(
                {
                    "edit": "Post deleted!",
                },
                status=201,
            )
        else:
            return JsonResponse({"error": "Invalid Post"}, status=400)

    return JsonResponse({"error": "Invalid Request"}, status=400)


@login_required
def following(request):
    # Get the user requested in the url and their posts
    follows_by_user = Follower.objects.filter(followed_by=request.user)
    followed_users = User.objects.filter(following__in=follows_by_user)
    posts = (
        Post.objects.filter(owner__in=followed_users)
        .annotate(like_count=Count("likes"))
        .order_by("-timestamp")
    )

    # Owned is none, since this view is for posts by followed users
    # We own nothing here!
    likes_by_user = Like.objects.filter(liker=request.user)
    liked_posts = Post.objects.filter(likes__in=likes_by_user)
    owned_posts = None

    # We meet again mr. paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Nice and neat!
    context = {
        "all_posts": posts,
        "liked_posts": liked_posts,
        "owned_posts": owned_posts,
        "page_obj": page_obj,
        "page_number": page_number,
        "page_range": paginator.page_range,
    }

    return render(request, "network/following.html", context)
