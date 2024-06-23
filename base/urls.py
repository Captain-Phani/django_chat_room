from django.urls import path
from . import views

urlpatterns = [
    path('login_page/', views.loginPage,name='login'),
    path('logout_page/', views.logoutPage,name='logout'),
    path('register/',views.registerUser, name='register'),
    path('home/', views.home, name='home'),   # url patterned named 'home'
    path('room/<str:pk>/', views.room, name='room'),    # url patterned named 'room'
    path('create_room/', views.create_room,name='create_room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete_room')
]

# Note:
# slashes should be at the end of the path not infront of them
# correct ex: home/
# wrong ex: /home