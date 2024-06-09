from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id': 1, 'room_name': 'Python'},
    {'id': 2, 'room_name': 'JavaScript'},
    {'id': 3, 'room_name': 'SQL'}
]
def home(request):

    return render(request, 'base/home.html', {'rooms': rooms}) # passing rooms list into template
    # return HttpResponse('Home')


def room(request, pk):

    room = None
    for elem in rooms:
        if elem['id'] == int(pk):
            room = elem

    context = {'room': room}
    return render(request, 'base/room.html', context)
    # return HttpResponse('Room')


