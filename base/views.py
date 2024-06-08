from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    return render(request, 'home.html')
    # return HttpResponse('Home')


def room(request):

    return render(request, 'room.html')
    # return HttpResponse('Room')


