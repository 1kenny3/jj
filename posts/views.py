from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.


def home(request):
    return HttpResponse("<h1>ку</h1>")


def about(request):
    name = "kkk"
    age = 12
    nnickname = "autyaga"
    response = f"<h1>{name}</h1> <br> <h2>{age}</h2> <p>{nnickname}</p>"
    return HttpResponse(response)


def test(request):
    return render(request, "index.html")


def kenny(request):
    return HttpResponse("<h1>они убили кенни</h1>")
