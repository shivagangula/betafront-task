from django.urls import path
from .views import PokemonListView, BattleAPIView, BattleStatusAPIView, BattleListView

urlpatterns = [
    path('', PokemonListView.as_view(), name='pokemon-list'),
    path('battle/', BattleListView.as_view(), name='battle-list'),
    path('battle/start/', BattleAPIView.as_view(), name='battle-start'),
    path('battle/<uuid:battle_id>/', BattleStatusAPIView.as_view(), name='battle-status'),
]
