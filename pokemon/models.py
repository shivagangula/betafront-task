from django.db import models
import uuid
from django.db.models import JSONField
from django.contrib.auth.models import UserManager


class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, null=True, blank=True)
    attributes = JSONField()  
    
    objects = UserManager()
    def __str__(self):
        return self.name


class Battle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pokemon_a = models.ForeignKey(Pokemon, related_name='pokemon_a', on_delete=models.CASCADE, blank=True, null=True)
    pokemon_b = models.ForeignKey(Pokemon, related_name='pokemon_b', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=50, default='BATTLE_INPROGRESS')
    result = models.JSONField(null=True, blank=True)