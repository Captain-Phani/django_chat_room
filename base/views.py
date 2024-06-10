from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RoomForm
from .models import Room, Message, Topic
# rooms = [
#     {'id': 1, 'room_name': 'Python'},
#     {'id': 2, 'room_name': 'JavaScript'},
#     {'id': 3, 'room_name': 'SQL'}
# ]


def home(request):
    # return render(request, 'base/home.html', {'rooms': rooms}) # passing rooms list into template
    # return HttpResponse('Home')

    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):
    # rooms = Room.objects.all()
    # print(rooms)
    # room = None
    # for elem in rooms:
    #     print(elem)
    #     if elem['id'] == int(pk):
    #         room = elem

    room = Room.objects.get(pk=pk)

    context = {'room': room}
    return render(request, 'base/room.html', context)
    # return HttpResponse('Room')


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST) # IT WILL PRING QUERY DICT ALONG WITH CSRF TOKEN AND DATA
        form = RoomForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()

            # redirect function will take one parameter to navigate to that page
            # In this home is paramter to navigate
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request,pk):

    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)    # creating an instance of form
    if request.method == 'POST':

        # we are sending the data to RoomForm to process for that particular instance
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            print("Successfully updated")
            form.save()
            return redirect('home')

    context= {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):

    room = Room.objects.get(pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/del_room.html', context)