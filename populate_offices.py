import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paperless_site.settings')
django.setup()

from tracking.models import Office
from tracking.choices import OFFICE_CHOICES

def run():
    print("="*50)
    print("POPULATING OFFICES")
    print("="*50)
    
    for code, name in OFFICE_CHOICES:
        office, created = Office.objects.get_or_create(
            office_code=code,
            defaults={'office_name': name}
        )
        if created:
            print(f"✓ Created: {name}")
        else:
            print(f"• Already exists: {name}")
    
    print("="*50)
    print(f"Total offices: {Office.objects.count()}")
    print("="*50)

if __name__ == "__main__":
    run()