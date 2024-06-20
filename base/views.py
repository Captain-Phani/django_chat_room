from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from base.forms import RoomForm
from .models import Room, Message, Topic


# rooms = [
#     {'id': 1, 'room_name': 'Python'},
#     {'id': 2, 'room_name': 'JavaScript'},
#     {'id': 3, 'room_name': 'SQL'}
# ]


def loginPage(request):
    """
    defines login functionality

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')  # fetching username from forms
        password = request.POST.get('password')  # fetching password from forms

        try:
            user = User.objects.get(username=username)  # getting User object based on fetched username

        except User.DoesNotExist:
            messages.error(request, "User does not exit")  # if object does not exist shows this error msg
            return render(request, 'base/login_form.html')

    # below step is to authenticate provided username and password and returns user object or else error
        user = authenticate(request, username=username, password=password)
        print(user)

        if user != None:

            login(request, user)  # login() will create a session in browser
            next_url = request.GET.get('next', home)
            return redirect(next_url)

        else:
            messages.error(request, "Username or password does not match")

    if 'next' in request.GET:

        print(request.GET)
        messages.info(request, "Login required to access this page")

    return render(request, 'base/login_form.html')


def logoutPage(request):
    """
    Logout page will remove the user session from browser session storage
    :param request:
    :return:
    """

    logout(request) # logout function will delete current user session from browser session storage
    return redirect('home')

def home(request):
    # return render(request, 'base/home.html', {'rooms': rooms}) # passing rooms list into template
    # return HttpResponse('Home')
    # q = request.GET.get('q') # fetches parameter

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Above condition if q is not none it returns q else it returns empty string

    # filters based on topic name with. first topic- foreign key second topic- navigates throgh foreign key and filters
    # name
    # filtered_rooms = Room.objects.filter(topic__topic_name=q)

    # icontains - it is case insensitive
    # contains - case sensitive
    # filtered_rooms = Room.objects.filter(topic__topic_name__icontains=q)
    filtered_rooms = Room.objects.filter(
        Q(topic__topic_name__icontains=q) |
        Q(room__icontains=q) |
        Q(description__icontains=q)

    )

    # Q Lookups are used when we need to combine two or more logical operations
    room_count = filtered_rooms.count()
    rooms = Room.objects.all()
    topic = Topic.objects.all()
    context = {'rooms': filtered_rooms, 'topic': topic, 'room_count': room_count}
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


@login_required(login_url='loginPage')
def create_room(request):
    """
    login_required is a decorator function to check if the current user is logged in

    if only user is logged in , current user has prevaliges to create a room

    create_room() funtion is created to create an individual room by using RoomForm()
    :param request:
    :return:
    """
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

@login_required(login_url='loginPage')
def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)  # creating an instance of form

    if request.user == room.host:
        return HttpResponse(f'You are not allowed here')

    if request.method == 'POST':

        # we are sending the data to RoomForm to process for that particular instance
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            print("Successfully updated")
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='loginPage')
def delete_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.user == room.host:
        return HttpResponse(f' you are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/del_room.html', context)


# Note for next_url and next in loginpage:
# When a user tries to access a view that requires authentication, the login_required decorator redirects the
# user to the login page and appends a next parameter to the URL. This next parameter contains the
# URL of the page the user was originally trying to access.

# For example, if the user tries to access /create_room/ without being logged in,
# they will be redirected to /loginPage/?next=/create_room/.


# request.GET is a dictionary-like object that contains all the GET parameters from the URL.
#
# get('next', 'home') attempts to retrieve the value of the next parameter from the URL.
#
# If the next parameter is present, its value (the URL the user originally wanted to visit)
# is assigned to next_url.
#
# If the next parameter is not present (i.e., the user directly accessed the login page
# without being redirected), it defaults to 'home'. This means that after a successful login, the user will be redirected to the home page.


#---------------------------------------------------------------
# Now we need to restrict users to modify rooms they created. they should not see the delete and edit options

# for ex: if user chat is logged in he is allowed to modify the rooms he created other than that  he is not allowed

# if the user is logged in he is not allowed to redirect login again while he was already logged in