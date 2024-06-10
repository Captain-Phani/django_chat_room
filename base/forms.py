from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"


# Django Modelform is a type of form which considers fields from model to fillup