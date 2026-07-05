import requests
import json

BASE_URL = "http://127.0.0.1:5000/inventory"

def print_separator():
    print("-" * 50)

def view_all():
    print_separator()
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("Inventory is currently empty.")
                return
            for item in items:
                p = item["product"]
                print(f"Barcode: {item['barcode']} | Name: {p['product_name']} | Brand: {p['brands']}")
                print(f"  Price: ${item['price']:.2f} | Stock: {item['quantity']} units")
                print_separator()
        else:
            print("Failed to pull data from server.")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the Flask server. Is it running?")

def view_item():
    barcode = input("Enter barcode to search: ").strip()
    if not barcode: return
    try:
        response = requests.get(f"{BASE_URL}/{barcode}")
        if response.status_code == 200:
            item = response.json()
            print(json.dumps(item, indent=2))
        else:
            print(f"Error: {response.json().get('error', 'Item not found.')}")
    except requests.exceptions.ConnectionError:
        print("Server connection error.")

def add_item():
    print("\n--- Add New Inventory Item ---")
    barcode = input("Enter Barcode (e.g., 737628005000): ").strip()
    if not barcode: return
    
    try:
        price = float(input("Enter Selling Price: "))
        quantity = int(input("Enter Initial Stock Quantity: "))
    except ValueError:
        print("Invalid numerical values. Aborting insertion.")
        return

    payload = {"barcode": barcode, "price": price, "quantity": quantity}
    
    try:
        print("Querying system endpoints and fetching OpenFoodFacts data details...")
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print("Item added successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed: {response.json().get('error', 'Unknown Error')}")
    except requests.exceptions.ConnectionError:
        print("Server connection error.")

def update_item():
    barcode = input("Enter barcode of the product to update: ").strip()
    if not barcode: return
    
    print("Leave empty and press Enter to keep current values.")
    price_in = input("Enter new price: ").strip()
    qty_in = input("Enter new quantity: ").strip()
    
    payload = {}
    if price_in:
        try: payload["price"] = float(price_in)
        except ValueError: print("Skipping price due to invalid format.")
    if qty_in:
        try: payload["quantity"] = int(qty_in)
        except ValueError: print("Skipping quantity due to invalid format.")

    if not payload:
        print("No changes specified.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/{barcode}", json=payload)
        if response.status_code == 200:
            print("Product dynamically updated successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed: {response.json().get('error', 'Update rejected.')}")
    except requests.exceptions.ConnectionError:
        print("Server connection error.")

def delete_item():
    barcode = input("Enter barcode of the item to permanently delete: ").strip()
    if not barcode: return
    
    confirm = input(f"Are you sure you want to delete {barcode}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Deletion canceled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/{barcode}")
        if response.status_code == 204:
            print("Product dropped from inventory database arrays successfully.")
        else:
            print("Error: Could not locate the target product.")
    except requests.exceptions.ConnectionError:
        print("Server connection error.")

def main_menu():
    while True:
        print("\n=== RETAIL INVENTORY MANAGEMENT PORTAL ===")
        print("1. View Full Inventory Summary")
        print("2. Search Item Details by Barcode")
        print("3. Register New Inventory Item (Pulls from OpenFoodFacts)")
        print("4. Update Item Price/Stock Levels")
        print("5. Delete Product Record")
        print("6. Exit Portal")
        
        choice = input("Select an option (1-6): ").strip()
        if choice == '1': view_all()
        elif choice == '2': view_item()
        elif choice == '3': add_item()
        elif choice == '4': update_item()
        elif choice == '5': delete_item()
        elif choice == '6': 
            print("Closing Admin Portal connection.")
            break
        else:
            print("Invalid entry. Please try again.")

if __name__ == '__main__':
    main_menu()