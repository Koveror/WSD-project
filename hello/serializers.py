from rest_framework import serializers
from . import models

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('name', 'price', 'numberSold', 'primarygenre', 'secondarygenre', 'dateCreated', 'URL', 'description')

