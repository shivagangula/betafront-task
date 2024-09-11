import csv
from pokemon.models import Pokemon
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Import Pokémon data from a CSV file into the database'

    def handle(self, *args, **options):
        csv_file = "/tmp/pokemon_data.csv"
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract fields
                name = row.get('name')
                type1 = row.get('type1')
                type2 = row.get('type2', '')
                
                # Extract JSON fields
                attributes = {key: value for key, value in row.items() if key not in ['name', 'type1', 'type2']}
                
                # Create or update Pokémon instance
                Pokemon.objects.update_or_create(
                    name=name,
                    type1=type1,
                    type2=type2,
                    defaults={'attributes': attributes}
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))
