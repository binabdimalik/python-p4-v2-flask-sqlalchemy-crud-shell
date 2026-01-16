from app import app
from models import db, Pet
from sqlalchemy import func

def run_demo():
    print("--- Starting CRUD Demo ---")
    
    with app.app_context():
        # Clean up any existing data
        print("\nCleaning up existing data...")
        try:
            Pet.query.delete()
            db.session.commit()
        except:
            db.session.rollback()
            pass
        
        # 1. CREATE
        print("\n--- CREATE ---")
        print("Creating Fido...")
        pet1 = Pet(name="Fido", species="Dog")
        # pet1.id is None here
        print(f"Before add/commit: id={pet1.id}")
        
        db.session.add(pet1)
        db.session.commit()
        print(f"After commit: id={pet1.id}")
        print(f"Created: {pet1}")

        print("\nCreating Whiskers...")
        pet2 = Pet(name="Whiskers", species="Cat")
        db.session.add(pet2)
        db.session.commit()
        print(f"Created: {pet2}")
        
        # 2. READ
        print("\n--- READ ---")
        print("Querying all pets...")
        all_pets = Pet.query.all()
        print(f"All pets: {all_pets}")
        
        print("\nQuerying first pet...")
        first_pet = Pet.query.first()
        print(f"First pet: {first_pet}")
        
        print("\nFiltering for Cats...")
        cats = Pet.query.filter_by(species='Cat').all()
        print(f"Cats: {cats}")
        
        print("\nFiltering for names starting with 'F'...")
        f_pets = Pet.query.filter(Pet.name.startswith('F')).all()
        print(f"F pets: {f_pets}")
        
        print("\nGetting by ID (using db.session.get)...")
        got_pet = db.session.get(Pet, pet1.id)
        print(f"Got pet by ID {pet1.id}: {got_pet}")

        print("\nCounting pets...")
        # Note: func.count usually requires a wrapper or scalar
        count = db.session.query(func.count(Pet.id)).scalar()
        print(f"Count: {count}")

        # 3. UPDATE
        print("\n--- UPDATE ---")
        print("Updating Fido to 'Fido the mighty'...")
        pet_to_update = db.session.get(Pet, pet1.id)
        if pet_to_update:
            pet_to_update.name = "Fido the mighty"
            # No need to add(), just commit
            db.session.commit()
            print(f"Updated: {pet_to_update}")
        
        # Check update
        check_pet = db.session.get(Pet, pet1.id)
        print(f"Verify Update: {check_pet.name}")

        # 4. DELETE
        print("\n--- DELETE ---")
        print(f"Deleting Fido ({pet1.id})...")
        pet_to_delete = db.session.get(Pet, pet1.id)
        if pet_to_delete:
            db.session.delete(pet_to_delete)
            db.session.commit()
            print("Deleted.")
        
        print(f"Pets remaining: {Pet.query.all()}")
        
        print("\nDeleting all remaining pets...")
        Pet.query.delete()
        db.session.commit()
        print(f"Pets remaining: {Pet.query.all()}")

    print("\n--- Demo Complete ---")

if __name__ == "__main__":
    run_demo()
