from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, 'home/home.html')


def references_view(request, *args, **kwargs):
    return render(request, 'references/references.html')
