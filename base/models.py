from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import SET_NULL


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic_name


class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, max_length=100, on_delete=models.SET_NULL, null=True)
    room = models.CharField(max_length=200, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room

    class Meta:
        ordering = ['-updated_at','-created_at'] # if we did not mention '-' symbol it will show updated rooms and then
                                            # created rooms


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message[:50]

