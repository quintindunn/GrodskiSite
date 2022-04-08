from django.shortcuts import render


def index(request):
    ctx = {}
    return render(request, template_name="home_page/index.html", context=ctx)
