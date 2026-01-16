"""
Regional Animal Shelter Management System (RASMS)
Author: Abhishek Sardar
Description: Menu-driven system to manage shelters, animals, adoptions, and revenue.
"""

import json

DATA_FILE = "shelters_data.json"


# -------------------- CLASSES --------------------

class Animal:
    def __init__(self, animal_id, animal_type, name, age, breed, health, status):
        self.id = animal_id
        self.type = animal_type
        self.name = name
        self.age = age
        self.breed = breed
        self.health = health
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "age": self.age,
            "breed": self.breed,
            "health": self.health,
            "status": self.status
        }


class Shelter:
    def __init__(self, name, location, address, revenue=0, adopted_count=0):
        self.name = name
        self.location = location
        self.address = address
        self.animals = []
        self.revenue = revenue
        self.adopted_count = adopted_count

    def add_animal(self, animal):
        self.animals.append(animal)

    def remove_animal(self, animal):
        self.animals.remove(animal)

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "address": self.address,
            "revenue": self.revenue,
            "adopted_count": self.adopted_count,
            "animals": [animal.to_dict() for animal in self.animals]
        }


# -------------------- FILE HANDLING --------------------

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        # Return empty structure or default if file doesn't exist
        return []

    shelters = []
    for s in data["shelters"]:
        shelter = Shelter(
            s["name"], s["location"], s["address"],
            s["revenue"], s["adopted_count"]
        )
        for a in s["animals"]:
            animal = Animal(
                a["id"], a["type"], a["name"],
                a["age"], a["breed"], a["health"], a["status"]
            )
            shelter.add_animal(animal)
        shelters.append(shelter)
    return shelters


def save_data(shelters):
    data = {"shelters": [shelter.to_dict() for shelter in shelters]}
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# -------------------- CORE LOGIC --------------------

def find_animal(shelters, animal_id):
    for shelter in shelters:
        for animal in shelter.animals:
            if animal.id == animal_id:
                return shelter, animal
    return None, None


def move_animal_core(shelters, animal_id, target_shelter_index):
    current_shelter, animal = find_animal(shelters, animal_id)
    if not animal:
        return False, "Animal not found."

    if target_shelter_index < 0 or target_shelter_index >= len(shelters):
        return False, "Invalid shelter index."

    new_shelter = shelters[target_shelter_index]
    
    if current_shelter == new_shelter:
        return False, "Animal is already in this shelter."

    current_shelter.remove_animal(animal)
    new_shelter.add_animal(animal)
    
    return True, {
        "animal_id": animal.id,
        "animal_name": animal.name,
        "from_shelter": current_shelter.name,
        "to_shelter": new_shelter.name
    }


def update_health_core(shelters, animal_id, new_health):
    _, animal = find_animal(shelters, animal_id)
    if not animal:
        return False, "Animal not found."
    
    animal.health = new_health
    return True, "Health updated."


def update_status_core(shelters, animal_id, new_status):
    _, animal = find_animal(shelters, animal_id)
    if not animal:
        return False, "Animal not found."
    
    animal.status = new_status
    return True, "Status updated."


def calculate_fee(animal):
    if animal.type == "Dog":
        return 300 if animal.age < 5 else 200
    elif animal.type == "Cat":
        return 250 if animal.age < 5 else 150
    else:
        return 150 if animal.age < 5 else 100


def adopt_animal_core(shelters, animal_id):
    shelter, animal = find_animal(shelters, animal_id)

    if not animal:
        return False, "Animal not found."
    
    if animal.status == "Adopted":
        return False, "Animal already adopted."

    fee = calculate_fee(animal)
    animal.status = "Adopted"
    shelter.revenue += fee
    shelter.adopted_count += 1

    return True, fee


# -------------------- CLI FUNCTIONS --------------------

def view_inventory(shelters):
    for shelter in shelters:
        print(f"\nShelter: {shelter.name} ({shelter.address})")
        if not shelter.animals:
            print("  No animals currently.")
        for a in shelter.animals:
            print(f"  {a.id} | {a.name} | {a.type} | {a.breed} | "
                  f"{a.age} yrs | {a.health} | {a.status}")


def cli_move_animal(shelters):
    animal_id = input("Enter Animal ID to move: ")
    
    # Check if animal exists before asking for shelter to mimic original flow better
    # or just ask for everything. Original flow checked animal first.
    curshelter, animal = find_animal(shelters, animal_id)
    if not animal:
        print("Animal not found.")
        return

    print("Available shelters:")
    for i, shelter in enumerate(shelters):
        print(f"{i + 1}. {shelter.name}")

    try:
        choice = int(input("Move to shelter number: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    success, result = move_animal_core(shelters, animal_id, choice)
    
    if success:
        print("\nMovement Record:")
        print(f"Animal: {result['animal_id']} - {result['animal_name']}")
        print(f"From: {result['from_shelter']}")
        print(f"To: {result['to_shelter']}")
    else:
        print(f"Error: {result}")


def cli_update_status(shelters):
    animal_id = input("Enter Animal ID: ")
    
    # Just check existence
    _, animal = find_animal(shelters, animal_id)
    if not animal:
        print("Animal not found.")
        return

    print("1. Update Health Status")
    print("2. Update Adoption Status")
    choice = input("Choose option: ")

    if choice == "1":
        new_health = input("Enter new health status: ")
        success, msg = update_health_core(shelters, animal_id, new_health)
        print(msg)
    elif choice == "2":
        new_status = input("Enter new adoption status: ")
        success, msg = update_status_core(shelters, animal_id, new_status)
        print(msg)
    else:
        print("Invalid option.")


def cli_adopt_animal(shelters):
    animal_id = input("Enter Animal ID to adopt: ")
    success, result = adopt_animal_core(shelters, animal_id)
    
    if success:
         print(f"Animal adopted successfully. Adoption fee: ${result}")
    else:
        print(result)


def revenue_report(shelters):
    total = 0
    print("\nShelter Revenue Report")
    for shelter in shelters:
        print(f"{shelter.name} | Adopted: {shelter.adopted_count} | "
              f"Revenue: ${shelter.revenue}")
        total += shelter.revenue
    print(f"Regional Total Revenue: ${total}")


# -------------------- MAIN MENU --------------------

def main_menu():
    shelters = load_data()

    while True:
        print("\n--- RASMS MAIN MENU ---")
        print("1. View Shelter Inventory")
        print("2. Move Animal Between Shelters")
        print("3. Update Animal Status")
        print("4. Adopt Animal")
        print("5. View Shelter Revenue Report")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            view_inventory(shelters)
        elif choice == "2":
            cli_move_animal(shelters)
        elif choice == "3":
            cli_update_status(shelters)
        elif choice == "4":
            cli_adopt_animal(shelters)
        elif choice == "5":
            revenue_report(shelters)
        elif choice == "6":
            save_data(shelters)
            print("Data saved. Thank you for using RASMS.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main_menu()
