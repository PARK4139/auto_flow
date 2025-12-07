

def generate_random_address_usa():
    import random
    street_number = random.randint(1, 9999)
    street_name = random.choice(['Main Street', 'Park Avenue', 'Oak Lane', 'Maple Avenue', 'Cedar Road'])
    city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
    state = random.choice(['California', 'Texas', 'Florida', 'New York', 'Illinois'])
    zip_code = random.randint(10000, 99999)
    return f"{street_number} {street_name}, {city}, {state} {zip_code}"
