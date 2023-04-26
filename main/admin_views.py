from django.shortcuts import render, redirect


def page_not_found(request, *args, **argv):
    return render(request, "main/404.html")


def internal_server_rerror(request, *args, **argv):
    return render(request, "main/500.html")
