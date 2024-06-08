from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id': 1, 'room_name': 'Python'},
    {'id': 2, 'room_name': 'JavaScript'},
    {'id': 3, 'room_name': 'SQL'}
]
def home(request):

    return render(request, 'home.html', {'rooms': rooms}) # passing rooms list into template
    # return HttpResponse('Home')


def room(request):

    return render(request, 'room.html')
    # return HttpResponse('Room')


