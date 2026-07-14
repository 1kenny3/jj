import re
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.forms import PostEditForm, PostForm
from posts.models import Comment, Like, Post
from django.http.request import HttpRequest

# Create your views here.


def kenny(request):
    return HttpResponse("<h1>они убили кенни</h1>")


def home(request):
    return HttpResponse("<h1>ку</h1>")


def about(request):
    name = "kkk"
    age = 12
    nnickname = "autyaga"
    response = f"<h1>{name}</h1> <br> <h2>{age}</h2> <p>{nnickname}</p>"
    return HttpResponse(response)


def post_list(request: HttpRequest):
    q = request.GET.get("q", None)

    posts = (
        Post.objects.filter(is_published=True)
        .select_related("user")
        .prefetch_related("comments")
    )

    if q:
        posts = posts.filter(title__icontains=q)

    post_count = posts.count()

    context_obh = {"posts": posts, "count": post_count}

    return render(request, "posts/post_list.html", context_obh)


@login_required
def post_create(request: HttpRequest):
    post_form = PostForm()
    if request.method == "POST":
        post = PostForm(request.POST, request.FILES)
        if post.is_valid():
            post_object = Post(**post.cleaned_data)
            post_object.user = request.user
            post_object.save()
            return redirect("post_list")
        for error in post.errors:
            print(error)
            print("*" * 5)
            print(type(error))
        return render(
            request, "posts/post_create.html", context={"errors": post.errors}
        )

    return render(request, "posts/post_create.html", context={"form": post_form})


@login_required
def my_post(request: HttpRequest):
    user = request.user
    posts = (
        Post.objects.filter(user=user)
        .select_related("user")
        .prefetch_related("comments")
        .all()
    )
    if q := request.GET.get("q", None):
        posts = posts.filter(title__icontains=q)

    post_count = posts.count()

    return render(
        request, "posts/post_list.html", context={"posts": posts, "count": post_count}
    )


def post_detail(request: HttpRequest, pk):
    post = (
        Post.objects.select_related("user")
        .prefetch_related("comments", "comments__user")
        .get(id=pk)
    )
    return render(request, "posts/post_detail.html", context={"post": post})


@login_required
def post_edit(request: HttpRequest, pk):
    post = Post.objects.select_related("user").get(id=pk)
    user = request.user

    if post.user != user:
        return render(request, "posts/post_detail.html", context={"post": post})

    if request.method == "POST":
        form = PostEditForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            if title := cleaned_data.get("title"):
                post.title = title
            if content := cleaned_data.get("content"):
                post.content = content
            if rate := cleaned_data.get("rate"):
                post.rate = rate
            if image := cleaned_data.get("image"):
                post.image = image
            post.save()
            return redirect("post_detail", pk=post.pk)

    return render(request, "posts/post_edit.html", context={"post": post})


def create_comment(request: HttpRequest, pk):
    post = Post.objects.select_related("user").get(id=pk)

    content = request.POST.get("content")
    comment = Comment(post=post, content=content)

    if request.user.is_anonymous:
        comment.user = None

    else:
        comment.user = request.user

    comment.save()

    return redirect("post_detail", pk=post.pk)


def post_like(request: HttpRequest, pk):
    post = Post.objects.select_related("user").get(id=pk)

    like_queryset = Like.objects.filter(user=request.user, post=post)
    if like_queryset.exists():
        like_queryset.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    return redirect("post_detail", pk=post.pk)
