from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from posts.form import PostForm
from posts.models import Post
from django.http.request import HttpRequest

# Create your views here.


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

    posts = Post.objects.filter(is_published=True)

    if q:
        posts = posts.filter(title__icontains=q)

    post_count = posts.count()

    context_obh = {"posts": posts, "count": post_count}

    return render(request, "posts/post_list.html", context_obh)


def post_create(request: HttpRequest):
    post_form = PostForm()
    if request.method.lower() == "post":
        post = PostForm(request.POST, request.FILES)
        if post.is_valid():
            post_object = Post(**post.cleaned_data)
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


def kenny(request):
    return HttpResponse("<h1>они убили кенни</h1>")

