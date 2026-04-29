import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allocation.models import Truck, Load

LOADS_DATA = [
    {"name": "PALETE-FRAGIL", "peso": 385, "alt": 2.18, "larg": 0.90, "comp": 1.60, "val": 6959, "quantidade": 10},
    {"name": "BOBINA-ACO", "peso": 7868, "alt": 1.75, "larg": 0.95, "comp": 1.21, "val": 14489, "quantidade": 2},
    {"name": "MAQUINARIO-PESADO", "peso": 5453, "alt": 1.90, "larg": 1.38, "comp": 2.48, "val": 45277, "quantidade": 1},
]

def seed():
    print("Clearing old loads...")
    Load.objects.all().delete()
    
    print("Seeding new loads with quantities...")
    for l in LOADS_DATA:
        Load.objects.create(**l)
    
    print("Seed complete.")

if __name__ == "__main__":
    seed()
