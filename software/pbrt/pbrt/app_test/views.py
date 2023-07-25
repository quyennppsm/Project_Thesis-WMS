from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from datetime import datetime

def index(request):
    now = datetime.now()

    return render(
        request,
        "app_test/index.html",
        {
            'title' : "App Test",
            'message' : "App test!",
            'content' : " on " + now.strftime("%A, %d %B, %Y at %X")
        }
    )

def about(request):
    return render(
        request,
        "app_test/about.html",
        {
            'title' : "About app test",
            'content' : "Example app page for app test."
        }
    )