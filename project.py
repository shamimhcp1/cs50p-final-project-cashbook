import csv
from tabulate import tabulate
from datetime import date, datetime
import re
import sys
import pandas as pd


def show_dashboard():
    print("\nWelcome to Cashbook Management System")
    print("Track Income & Expenses,")
    print("add cash in and cash out entries,")
    print("and find overall cash in / cash out & balance instantly.\n")


def show_menu():
    menu = [
        ["Add Cash In", 1],
        ["Add Cash Out", 2],
        ["Manage Entries", 3],
        ["Manage Categories", 4],
        ["Show Balance", 5],
    ]

    headers = ["Menu Item", "Number"]
    print(tabulate(menu, tablefmt="grid", headers=headers))

    while True:
        try:
            try:
                n = int(input("Choose from menu (1-5): ").strip())
                if 1 <= n <= 5:
                    if n == 1:
                        add_cash_in()
                    elif n == 2:
                        add_cash_out()
                    elif n == 3:
                        manage_entries()
                    elif n == 4:
                        manage_categories()
                    elif n == 5:
                        get_balance()
                    break
            except ValueError:
                pass
        except EOFError:
            sys.exit("\n")


def add_cash_in():
    print("ADD CASH IN ENTRIES")

    entry_info = get_entry_info(1)
    if entry_info:
        create_entry(entry_info)
        print("Cash In entry added successfully.")


def add_cash_out():
    print("ADD CASH OUT ENTRIES")
    entry_info = get_entry_info(2)
    if entry_info:
        create_entry(entry_info)
        print("Cash Out entry added successfully.")

# ask user for entry info
def get_entry_info(entry_type):
    while True:
        try:
            amount = int(input("Enter Amount: ").strip())
            break
        except ValueError:
            pass

    remarks = input("Enter Remarks: ").strip()

    categories = get_categories()
    for cat in categories:
        print(cat['id'], cat['category'], end=", ")
    print()

    while True:
        try:
            cat_id = int(input("Enter Category Id: ").strip())
            if any(cat["id"] == str(cat_id) for cat in categories):
                break
        except ValueError:
            pass

    while True:
        date_input = input("Enter Date (yyyy-mm-dd): ").strip()
        if date_input:
            date_in = validate_date(date_input)
            if date_in:
                break
        else:
            date_in = date.today()
            break

    entries = get_entries()
    last_entry_id = max(int(entry["id"]) for entry in entries) if entries else 0

    return {
                "id": last_entry_id,
                "type_id": entry_type,
                "category_id": cat_id,
                "amount": amount,
                "remarks": remarks,
                "date": date_in,
            }

# create entry to entries.csv
def create_entry(entry_info):

    with open(entries_csv_path, "a") as file:
        fieldnames = ["id", "type_id", "category_id", "amount", "remarks", "date"]
        entries_writer = csv.DictWriter(file, fieldnames=fieldnames)
        entries_writer.writerow(
            {
                "id": entry_info['id'] + 1,
                "type_id": entry_info['type_id'],
                "category_id": entry_info['category_id'],
                "amount": entry_info['amount'],
                "remarks": entry_info['remarks'],
                "date": entry_info['date'],
            }
        )

    return True


def validate_date(date_input):
    match = re.search(r"^(\d{4}-\d{2}-\d{2})$", date_input)
    if match:
        try:
            datetime_obj = datetime.strptime(match.group(1), "%Y-%m-%d")
            date_obj = datetime_obj.date()
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            pass


def manage_entries():
    menu = [["Edit Entries", 1], ["Delete Entries", 2], ["View Entries", 3]]

    headers = ["Menu Item", "Number"]
    print(tabulate(menu, tablefmt="grid", headers=headers))

    while True:
        try:
            n = int(input("Choose from menu (1-3): ").strip())
            if 1 <= n <= 3:
                if n == 1:
                    edit_entry()
                elif n == 2:
                    delete_entry()
                elif n == 3:
                    print("VIEW ENTRIES")
                    view_all_entries()
                break
        except ValueError:
            pass


def edit_entry():
    print("Edit ENTRIES")
    view_all_entries()

    entry_found = False
    while True:
        try:
            entry_id = int(input("Enter 'id' to edit (or -1 to quit): ").strip())
            if entry_id == -1:
                sys.exit()
            single_entry = view_single_entry(entry_id)
            if single_entry:
                entry_found = True
            if not entry_found:
                print(f"\n*** id: {entry_id} not exist!***\n")
            else:
                break
        except ValueError:
            pass

    if entry_found:
        print("\nYou've selected below entry:")
        print(tabulate([single_entry], tablefmt="grid"))

    types = get_types()
    print("\nChoose from list of Types:")
    for entry_type in types:
        print(entry_type["id"], entry_type["type"], end=", ")
    print("\n")

    type_found = False
    while True:
        try:
            type_id_input = input("Update 'type id' (or -1 to quit): ").strip()
            if not type_id_input:
                break
            type_id = int(type_id_input)
            if type_id == -1:
                sys.exit()
            if any(entry_type["id"] == str(type_id) for entry_type in types):
                type_found = True
            if not type_found:
                print(f"\n*** id: {type_id} not exist!***\n")
            else:
                break
        except ValueError:
            pass

    categories = get_categories()
    print("\nChoose from List of Categories")
    for category in categories:
        print(category["id"], category["category"], end=", ")
    print("\n")

    category_found = False
    while True:
        try:
            category_id_input = input("Update 'category id' (or -1 to quit): ").strip()
            if not category_id_input:
                break
            category_id = int(category_id_input)
            if category_id == -1:
                sys.exit()
            if any(cat["id"] == str(category_id) for cat in categories):
                category_found = True
            if not category_found:
                print(f"\n*** id: {category_id} not exist!***\n")
            else:
                break
        except ValueError:
            pass

    amount_found = False
    while True:
        try:
            amount_input = input("\nUpdate 'amount' (or -1 to quit): ").strip()
            if not amount_input:
                break
            amount = int(amount_input)
            if amount == -1:
                sys.exit()
            else:
                amount_found = True
                break
        except ValueError:
            pass

    remarks_found = False
    while True:
        try:
            remarks = input("\nUpdate 'remarks' (or -1 to quit): ").strip()
            if not remarks:
                break
            elif remarks == "-1":
                sys.exit()
            else:
                remarks_found = True
                break
        except ValueError:
            pass

    update_date = False
    while True:
        date_input = input("\nUpdate Date (yyyy-mm-dd) (or -1 to quit): ").strip()
        if not date_input:
            break
        elif date_input == "-1":
            sys.exit()
        else:
            new_date = validate_date(date_input)
            if new_date:
                update_date = True
                break

    if not type_found:
        type_id = None

    if not category_found:
        category_id = None

    if not amount_found:
        amount = None

    if not remarks_found:
        remarks = None

    if not update_date:
        new_date = None

    entry_info = {
                "id": entry_id,
                "type_id": type_id,
                "category_id": category_id,
                "amount": amount,
                "remarks": remarks,
                "date": new_date,
            }

    if update_entry(entry_info):
        print("\nEntry updated successfully.\n")


def update_entry(entry_info):

    entries = get_entries()
    for entry in entries:
        if entry["id"] == str(entry_info['id']):

            if entry_info['type_id']:
                entry["type_id"] = entry_info['type_id']
            if entry_info['category_id']:
                entry["category_id"] = entry_info['category_id']
            if entry_info['amount']:
                entry["amount"] = entry_info['amount']
            if entry_info['remarks']:
                entry["remarks"] = entry_info['remarks']
            if entry_info['date']:
                entry["date"] = entry_info['date']

            with open(entries_csv_path, mode="w", newline="") as file:
                fieldnames = ["id", "type_id", "category_id", "amount", "remarks", "date"]
                entries_writer = csv.DictWriter(file, fieldnames=fieldnames)
                entries_writer.writeheader()
                entries_writer.writerows(entries)

            return True


def delete_entry():
    print("Delete ENTRIES")
    view_all_entries()

    entry_found = False
    while True:
        try:
            entry_id = int(input("Enter 'id' to delete (or -1 to quit): ").strip())
            if entry_id == -1:
                sys.exit()
            single_entry = view_single_entry(entry_id)
            if single_entry:
                entry_found = True
            if not entry_found:
                print(f"\n*** id: {entry_id} not exist!***\n")
            else:
                break
        except ValueError:
            pass

    if entry_found:
        print("\nYou've selected below entry:")
        print(tabulate([single_entry], tablefmt="grid"))

    confirm_found = False
    while True:
        try:
            confirm = input("\nAre you sure do delete? 'yes' (or -1 to quit): ").strip()
            if confirm == "-1":
                sys.exit()
            elif confirm == "yes":
                confirm_found = True
                break
        except ValueError:
            pass

    if confirm_found:
        if delete_single_entry(entry_id):
            print("\nEntry deleted successfully.\n")


def delete_single_entry(entry_id):
    df = pd.read_csv(entries_csv_path)
    df = df[df["id"] != entry_id]
    df.to_csv(entries_csv_path, index=False)
    return True


def view_all_entries():
    types = get_types()
    categories = get_categories()
    entries = get_entries()
    modified_entries = []

    for row in entries:
        for entry_type in types:
            if entry_type["id"] == row["type_id"]:
                row["type_id"] = entry_type["type"]

        for cat in categories:
            if cat["id"] == row["category_id"]:
                row["category_id"] = cat["category"]

        modified_entries.append(row)

    print(tabulate(modified_entries, tablefmt="grid"))


def view_single_entry(entry_id):
    entries = get_entries()
    types = get_types()
    categories = get_categories()

    for entry in entries:
        if int(entry["id"]) == entry_id:
            for entry_type in types:
                if entry_type["id"] == entry["type_id"]:
                    entry["type_id"] = entry_type["type"]
            for cat in categories:
                if cat["id"] == entry["category_id"]:
                    entry["category_id"] = cat["category"]
            return entry


def manage_categories():
    menu = [
        ["Add Category", 1],
        ["Edit Category", 2],
        ["Delete Category", 3],
        ["View Categories", 4],
    ]

    headers = ["Menu Item", "Number"]
    print(tabulate(menu, tablefmt="grid", headers=headers))

    while True:
        try:
            n = int(input("Choose from menu (1-4): ").strip())
            if 1 <= n <= 4:
                if n == 1:
                    add_category()
                elif n == 2:
                    edit_category()
                elif n == 3:
                    delete_category()
                elif n == 4:
                    print("VIEW CATEGORIES")
                    view_all_categories()
                break
        except ValueError:
            pass


def add_category():
    while True:
        try:
            category_name = input("\nEnter category name (or -1 to quit): ").strip()

            if category_name:
                if category_name == "-1":
                    break
                else:
                    categories = get_categories()
                    last_id = (
                        max(int(cat["id"]) for cat in categories) if categories else 0
                    )

                    with open(categories_csv_path, "a") as file:
                        fieldnames = ["id", "category"]
                        entries_writer = csv.DictWriter(file, fieldnames=fieldnames)
                        entries_writer.writerow(
                            {"id": last_id + 1, "category": category_name}
                        )

                    print("\nCategory added successfully.\n")
                    break
            else:
                raise ValueError

        except ValueError:
            pass


def edit_category():
    print("EDIT CATEGORY")
    view_all_categories()

    entry_found = False
    while True:
        try:
            entry_id = int(input("Enter 'id' to edit (or -1 to quit): ").strip())
            if entry_id == -1:
                sys.exit()
            single_entry = view_single_category(entry_id)
            if single_entry:
                entry_found = True
            if not entry_found:
                print(f"\n*** id: {entry_id} not exist!***\n")
            else:
                break
        except ValueError:
            pass

    if entry_found:
        print("\nYou've selected below category:")
        print(tabulate([single_entry], tablefmt="grid"))

    while True:
        try:
            category_name = input("\nEnter category name (or -1 to quit): ").strip()
            if category_name:
                if category_name == "-1":
                    sys.exit()
                break
            else:
                raise ValueError

        except ValueError:
            pass

    if update_category(entry_id, category_name):
        print("\nCategory updated successfully.\n")


def update_category(entry_id, category_name):
    categories = []
    with open(categories_csv_path, mode="r") as file:
        categories_reader = csv.DictReader(file)
        for row in categories_reader:
            categories.append(row)

    for category in categories:
        if category["id"] == str(entry_id):
            category["category"] = category_name

    with open(categories_csv_path, mode="w", newline="") as file:
        fieldnames = ["id", "category"]
        categories_writer = csv.DictWriter(file, fieldnames=fieldnames)
        categories_writer.writeheader()
        categories_writer.writerows(categories)

    return True


def view_single_category(entry_id):
    categories = get_categories()

    for category in categories:
        if category["id"] == str(entry_id):
            return category


def delete_category():
    print("DELETE CATEGORY")
    view_all_categories()

    entry_found = False
    while True:
        try:
            entry_id = int(input("Enter 'id' to delete (or -1 to quit): ").strip())
            if entry_id == -1:
                sys.exit()
            single_entry = view_single_category(entry_id)
            if single_entry:
                entry_found = True
            if not entry_found:
                print(f"\n*** id: {entry_id} not exist!***\n")
            else:
                break
        except ValueError:
            pass

    if entry_found:
        print("\nYou've selected below category:")
        print(tabulate([single_entry], tablefmt="grid"))

    confirm_found = False
    while True:
        try:
            confirm = input("\nAre you sure do delete? 'yes' (or -1 to quit): ").strip()
            if confirm == "-1":
                sys.exit()
            elif confirm == "yes":
                confirm_found = True
                break
        except ValueError:
            pass

    if confirm_found:
        if delete_single_category(entry_id):
            print("\nCategory deleted successfully.\n")


def delete_single_category(entry_id):
    df = pd.read_csv(categories_csv_path)
    df = df[df["id"] != entry_id]
    df.to_csv(categories_csv_path, index=False)
    return True


def view_all_categories():
    categories = []

    with open(categories_csv_path, mode="r", newline="") as file:
        categories_csv_reader = csv.reader(file)
        for row in categories_csv_reader:
            categories.append({"id": row[0], "category": row[1]})

    print(tabulate(categories, tablefmt="grid"))


def get_balance():
    entries = get_entries()
    cash_in = 0
    cash_out = 0

    for data in entries:
        if data["type_id"] == str(1):
            cash_in += int(data["amount"])
        if data["type_id"] == str(2):
            cash_out += int(data["amount"])

    net_balance = cash_in - cash_out

    balance = [
        ["Net Balance", str(net_balance) + " Tk"],
        ["Total In (+)", str(cash_in) + " Tk"],
        ["Total Out (-)", str(cash_out) + " Tk"],
    ]
    print(tabulate(balance, tablefmt="grid"))


def get_categories():
    categories = []

    with open(categories_csv_path, mode="r", newline="") as file:
        categories_csv_reader = csv.reader(file)
        next(categories_csv_reader, None)
        for row in categories_csv_reader:
            categories.append({"id": row[0], "category": row[1]})

    return categories


def get_types():
    types = []

    with open(types_csv_path, mode="r", newline="") as file:
        types_csv_reader = csv.reader(file)
        next(types_csv_reader, None)
        for row in types_csv_reader:
            types.append({"id": row[0], "type": row[1]})

    return types


def get_entries():
    entries = []

    with open(entries_csv_path, mode="r", newline="") as file:
        entries_csv_reader = csv.reader(file)
        next(entries_csv_reader, None)
        for row in entries_csv_reader:
            entries.append(
                {
                    "id": row[0],
                    "type_id": row[1],
                    "category_id": row[2],
                    "amount": row[3],
                    "remarks": row[4],
                    "date": row[5],
                }
            )

    return entries


# global variables
categories_csv_path = "csv_folder/categories.csv"
entries_csv_path = "csv_folder/entries.csv"
types_csv_path = "csv_folder/types.csv"

def main():
    show_dashboard()
    show_menu()

if __name__ == "__main__":
    main()
