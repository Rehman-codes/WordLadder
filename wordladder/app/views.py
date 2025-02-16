from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, "base.html")

def mode(request):
    return render(request, "mode.html")

def challenge(request):
    return render(request, "challenge.html")

def playground(request, challenge_id):
    return render(request, "playground.html")