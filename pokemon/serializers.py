from rest_framework import serializers
from .models import Pokemon, Battle

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'

class BattleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Battle
        fields = '__all__'
