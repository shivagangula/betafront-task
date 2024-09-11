from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pokemon, Battle
from .serializers import PokemonSerializer, BattleSerializer
from .tasks import battle_simulator_task
import uuid


import logging
logger = logging.getLogger(__name__)

class PokemonListView(generics.ListAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    

class BattleListView(generics.ListAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    
    
class BattleAPIView(APIView):
    def post(self, request):
    
        try:
           pokemon_a = Pokemon.objects.get(name__iexact=request.data.get('pokemon_a'))
        except Pokemon.DoesNotExist:
            pokemon_a = None
        
        try:
           pokemon_b = Pokemon.objects.get(name__iexact=request.data.get('pokemon_b'))
        except Pokemon.DoesNotExist:
            pokemon_b = None
            
        if not pokemon_a and not pokemon_b:
            return Response({"status": "POKEMONS_NOT_VAILD"}, status=status.HTTP_404_NOT_FOUND)
        
        battle_id = uuid.uuid4()
        battle = Battle.objects.create(pokemon_a=pokemon_a, pokemon_b=pokemon_b, id=battle_id)

        # Trigger async battle
        battle_simulator_task.delay(battle.id)
        return Response({"status":"BATTLE_INPROGRESS","battle_id": battle_id})

class BattleStatusAPIView(APIView):
    def get(self, request, battle_id):
        try:
            battle = Battle.objects.get(id=battle_id)
            return Response({
                "status": battle.status,
                "result": battle.result
            })
        except Battle.DoesNotExist as e:
            logger.error(e)
            return Response({"status": "BATTLE_NOI_FOUND"}, status=status.HTTP_404_NOT_FOUND)
