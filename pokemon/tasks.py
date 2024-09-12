from celery import shared_task
from .models import Battle
import logging
logger = logging.getLogger(__name__)

class BattleSimulator:
    def __init__(self, battle_id):
        self.battle_id = battle_id
        self.battle = None
        self.pokemon_a = None
        self.pokemon_b = None
        self.winner = None
        self.won_by_margin = 0
    
    def load_battle(self):
        
        self.battle = Battle.objects.get(id=self.battle_id)
        self.pokemon_a = self.battle.pokemon_a
        self.pokemon_b = self.battle.pokemon_b
        

    def calculate_damage(self, attacker, defender):

        attacker_type1 = attacker.type1  
        attacker_type2 = attacker.type2  
        attacker_attack = float(attacker.attributes['attack'])

        defender_against_type1 = float(defender.attributes.get(f"against_{attacker_type1}", 1))
        defender_against_type2 = float(defender.attributes.get(f"against_{attacker_type2}", 1))

        if defender_against_type2:
            damage = (attacker_attack / 200) * 100 - (((defender_against_type1 / 4) * 100) + ((defender_against_type2 / 4) * 100))
        else:
            damage = (attacker_attack / 200) * 100 - ((defender_against_type1 / 4) * 100)
        return damage
        
    def simulate(self):
        try:
            self.load_battle()
            
            if not self.pokemon_a and self.pokemon_a:
                damage_a_to_b = 0
                damage_b_to_a = 1
            
            if not self.pokemon_b and self.pokemon_a:
                damage_a_to_b = 1
                damage_b_to_a = 0
                
            
            if self.pokemon_a and self.pokemon_b:
                # Round 1 - Pokemon A attacks Pokemon B
                damage_a_to_b = self.calculate_damage(self.pokemon_a, self.pokemon_b)
    
                # Round 2 - Pokemon B attacks Pokemon A
                damage_b_to_a = self.calculate_damage(self.pokemon_b, self.pokemon_a)
            

            # Determine winner
            if damage_a_to_b > damage_b_to_a:
                self.winner = getattr(self.pokemon_a, 'name', None)
                self.won_by_margin =  damage_a_to_b - damage_b_to_a
            elif damage_b_to_a > damage_a_to_b:
                self.winner = getattr(self.pokemon_b, 'name', None)
                self.won_by_margin = damage_b_to_a - damage_a_to_b
            else:
                self.winner = "Draw"
                self.won_by_margin = 0

            self.battle.result = {
                "winnerName": self.winner,
                "wonByMargin": self.won_by_margin
            }
            self.battle.status = "BATTLE_COMPLETED"
            self.battle.save()
            return {
                "winnerName": self.winner,
                "wonByMargin": self.won_by_margin
            }
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            if self.battle:
                self.battle.status = "BATTLE_FAILED"
                self.battle.save()
            return {
                "winnerName": self.winner or "None",
                "wonByMargin": self.won_by_margin,
                'e':e
            }

# Celery task
@shared_task
def battle_simulator_task(battle_id):
    simulator = BattleSimulator(battle_id)
    simulator.simulate()
    return {'status':'task done'}
