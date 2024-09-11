from rest_framework.test import APITestCase
from rest_framework import status
from .models import Pokemon, Battle
from django.urls import reverse
from .tasks import BattleSimulator
import uuid


class PokemonListViewTests(APITestCase):
    def setUp(self):
        self.battle_id = None
        self.pokemon1 = Pokemon.objects.create(name="Bulbasaur", type1="grass", type2="poison", attributes={
            "hp": "45",
            "speed": "45",
            "attack": "49",
            "defense": "49",
            "height_m": "0.7",
            "abilities": "['Overgrow', 'Chlorophyll']",
            "sp_attack": "65",
            "weight_kg": "6.9",
            "base_total": "318",
            "generation": "1",
            "sp_defense": "65",
            "against_bug": "1",
            "against_ice": "2",
            "against_dark": "1",
            "against_fire": "2",
            "against_rock": "1",
            "capture_rate": "45",
            "is_legendary": "0",
            "against_fairy": "0.5",
            "against_fight": "0.5",
            "against_ghost": "1",
            "against_grass": "0.25",
            "against_steel": "1",
            "against_water": "0.5",
            "classfication": "Seed Pokémon",
            "japanese_name": "Fushigidaneフシギダネ",
            "against_dragon": "1",
            "against_flying": "2",
            "against_ground": "1",
            "against_normal": "1",
            "against_poison": "1",
            "base_egg_steps": "5120",
            "base_happiness": "70",
            "pokedex_number": "1",
            "against_psychic": "2",
            "percentage_male": "88.1",
            "against_electric": "0.5",
            "experience_growth": "1059860"
        })
        self.pokemon2 = Pokemon.objects.create(name="Charmander", type1="fire", type2=None, attributes={
            "hp": "39",
            "speed": "65",
            "attack": "52",
            "defense": "43",
            "height_m": "0.6",
            "abilities": "['Blaze', 'Solar Power']",
            "sp_attack": "60",
            "weight_kg": "8.5",
            "base_total": "309",
            "generation": "1",
            "sp_defense": "50",
            "against_bug": "0.5",
            "against_ice": "0.5",
            "against_dark": "1",
            "against_fire": "0.5",
            "against_rock": "2",
            "capture_rate": "45",
            "is_legendary": "0",
            "against_fairy": "0.5",
            "against_fight": "1",
            "against_ghost": "1",
            "against_grass": "0.5",
            "against_steel": "0.5",
            "against_water": "2",
            "classfication": "Lizard Pokémon",
            "japanese_name": "Hitokageヒトカゲ",
            "against_dragon": "1",
            "against_flying": "1",
            "against_ground": "2",
            "against_normal": "1",
            "against_poison": "1",
            "base_egg_steps": "5120",
            "base_happiness": "70",
            "pokedex_number": "4",
            "against_psychic": "1",
            "percentage_male": "88.1",
            "against_electric": "1",
            "experience_growth": "1059860"
        })
        
    def create_battle(self, pokemon_a_name, pokemon_b_name):
        data = {'pokemon_a': pokemon_a_name, 'pokemon_b': pokemon_b_name}
        response = self.client.post(reverse('battle-start'), data, format='json')
        return response
    
    def test_pokemon_str_method_case(self):
        self.assertEqual(str(self.pokemon1), "Bulbasaur")
        self.assertEqual(str(self.pokemon2), "Charmander")

    def test_battle_api_success_case(self):
       
        response = self.create_battle('Bulbasaur', 'Charmander')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'BATTLE_INPROGRESS')
    
    def test_battle_api_pokeman_not_valid_case(self):
       
        response = self.create_battle('Squirtle', 'Wartortle')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'POKEMONS_NOT_VAILD')

    def test_battle_api_accept_atleast_one_pokemon_case(self):
       
        response = self.create_battle('Bulbasaur', 'Wartortle')
        self.battle_id = response.data.get('battle_id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'BATTLE_INPROGRESS')
    
    def test_battle_api_not_found_case(self):
        response = self.client.get(reverse('battle-status', args=[uuid.uuid4()]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'BATTLE_NOI_FOUND')

    def test_simulation_fun_success_case(self):
       
        response = self.create_battle('Bulbasaur', 'Charmander')
        self.battle_id = response.data.get('battle_id')

        simulator = BattleSimulator(self.battle_id)
        simulator.simulate()

        
        battle = Battle.objects.get(id=self.battle_id)
        self.assertEqual(battle.status, 'BATTLE_COMPLETED')
    
    def test_simulation_fun_missing_case(self):
       
        response = self.create_battle('Bulbasaur', 'Wartortle')
        self.battle_id = response.data.get('battle_id')

       
        simulator = BattleSimulator(self.battle_id)
        simulator.simulate()

        
        battle = Battle.objects.get(id=self.battle_id)
        self.assertEqual(battle.status, 'BATTLE_COMPLETED')