import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allocation.models import Truck, Load

TRUCKS_DATA = [
    {"nome": "Semireboque-01", "cap_peso": 28000, "alt": 2.9, "larg": 2.5, "comp": 14.5},
    {"nome": "Semireboque-02", "cap_peso": 25000, "alt": 2.8, "larg": 2.4, "comp": 13.5},
    {"nome": "Frigorifico-01", "cap_peso": 22000, "alt": 2.6, "larg": 2.3, "comp": 13.0},
    {"nome": "Frigorifico-02", "cap_peso": 20000, "alt": 2.55, "larg": 2.25, "comp": 12.5},
    {"nome": "Bitren-01", "cap_peso": 42000, "alt": 3.0, "larg": 2.6, "comp": 25.0},
    {"nome": "Bitren-02", "cap_peso": 38000, "alt": 2.9, "larg": 2.5, "comp": 24.0},
    {"nome": "Rodotrem-01", "cap_peso": 57000, "alt": 3.2, "larg": 2.6, "comp": 30.0},
    {"nome": "Truck-01", "cap_peso": 15000, "alt": 2.7, "larg": 2.4, "comp": 10.0},
    {"nome": "Truck-02", "cap_peso": 13000, "alt": 2.6, "larg": 2.3, "comp": 9.0},
    {"nome": "VUC-01", "cap_peso": 8000, "alt": 2.4, "larg": 2.1, "comp": 7.0}
]

LOADS_DATA = [
    {"name": "PAL-001", "peso": 385, "alt": 2.18, "larg": 0.90, "comp": 1.60, "val": 6959},
    {"name": "PAL-002", "peso": 363, "alt": 1.85, "larg": 0.95, "comp": 1.21, "val": 13826},
    {"name": "PAL-003", "peso": 1166, "alt": 1.56, "larg": 0.99, "comp": 1.24, "val": 13781},
    {"name": "BOB-061", "peso": 7868, "alt": 1.75, "larg": 0.95, "comp": 1.21, "val": 14489},
    {"name": "MAQ-111", "peso": 5453, "alt": 1.90, "larg": 1.38, "comp": 2.48, "val": 45277},
    {"name": "ELE-161", "peso": 651, "alt": 0.78, "larg": 0.82, "comp": 0.51, "val": 27824},
    {"name": "GRA-221", "peso": 7883, "alt": 0.97, "larg": 2.28, "comp": 4.69, "val": 16615},
    {"name": "CON-261", "peso": 9639, "alt": 2.19, "larg": 2.22, "comp": 4.24, "val": 17004},
]

def seed():
    print("Seeding trucks...")
    for t in TRUCKS_DATA:
        Truck.objects.get_or_create(**t)
    
    print("Seeding loads...")
    for l in LOADS_DATA:
        Load.objects.get_or_create(**l)
    
    print("Seed complete.")

if __name__ == "__main__":
    seed()
