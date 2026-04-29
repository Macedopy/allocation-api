import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allocation.viewmodels import AllocationViewModel

def test_allocation():
    print("Initializing ViewModel...")
    viewmodel = AllocationViewModel()
    
    print("Running allocation algorithm...")
    result = viewmodel.get_allocation_plan()
    
    print("\nAllocation Result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_allocation()
