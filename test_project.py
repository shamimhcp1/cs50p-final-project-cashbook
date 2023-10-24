from project import validate_date, get_entries, get_categories, get_types, create_entry, update_entry
import random

# test validate date
def test_validate_date_valid_date():
    assert validate_date("2023-10-05") == "2023-10-05"

def test_validate_date_invalid_date():
    assert validate_date("2023-09-31") == None

def test_validate_date_invalid_format():
    assert validate_date("2023/09/10") == None

# test add_cash_in
def test_create_entry_cash_in():
    entries = get_entries()
    last_entry_id = max(int(entry["id"]) for entry in entries) if entries else 0
    assert create_entry({
                "id": last_entry_id,
                "type_id": 1,
                "category_id": 2,
                "amount": 200,
                "remarks": "Pytest cash in entry",
                "date": "2023-10-05",
            }) == True


# test add_cash_out
def test_create_entry_cash_out():
    entries = get_entries()
    last_entry_id = max(int(entry["id"]) for entry in entries) if entries else 0
    assert create_entry({
                "id": last_entry_id,
                "type_id": 2,
                "category_id": 2,
                "amount": 400,
                "remarks": "Pytest cash out entry",
                "date": "2022-11-10",
            }) == True


# Update an entry
def test_update_entry():

    entry_id = []
    entries = get_entries()
    for entry in entries:
        entry_id.append(entry['id'])

    type_id = []
    types = get_types()
    for type in types:
        type_id.append(type['id'])

    category_id = []
    categories = get_categories()
    for category in categories:
        category_id.append(category['id'])

    random_entry_id = random.choice(entry_id)
    random_type_id = random.choice(type_id)
    random_category_id = random.choice(category_id)

    assert update_entry({
                "id": random_entry_id,
                "type_id": random_type_id,
                "category_id": random_category_id,
                "amount": random.randint(1000, 9999),
                "remarks": "Pytest random update entry",
                "date": "2022-11-10",
            }) == True