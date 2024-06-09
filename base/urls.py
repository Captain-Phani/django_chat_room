from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),   # url patterned named 'home'
    path('room/<str:pk>/', views.room, name='room')    # url patterned named 'room'
]

# Note:
# slashes should be at the end of the path not infront of them
# correct ex: home/
# wrong ex: /home