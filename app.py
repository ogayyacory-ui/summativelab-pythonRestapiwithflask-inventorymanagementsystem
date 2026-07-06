from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mock database simulating the OpenFoodFacts payload format structured in an array
mock_db = [
    {
        "barcode": "008000000661",
        "price": 3.99,
        "quantity": 45,
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt"
        }
    },
    {
        "barcode": "737628005000",
        "price": 1.49,
        "quantity": 120,
        "status": 1,
        "product": {
            "product_name": "Coca-Cola Classic",
            "brands": "Coca-Cola",
            "ingredients_text": "Carbonated water, high fructose corn syrup, caramel color, phosphoric acid, natural flavors, caffeine"
        }
    },
    {
        "barcode": "012000161155",
        "price": 2.99,
        "quantity": 75,
        "status": 1,
        "product": {
            "product_name": "Kellogg's Frosted Flakes",
            "brands": "Kellogg's",
            "ingredients_text": "Corn, sugar, malt flavoring, salt, vitamins and minerals"
        }
    }
]

def fetch_openfoodfacts_data(barcode):
    """
    Queries the external OpenFoodFacts API to extract supplemental product metadata.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                return {
                    "product_name": data["product"].get("product_name", "Unknown Product"),
                    "brands": data["product"].get("brands", "Unknown Brand"),
                    "ingredients_text": data["product"].get("ingredients_text", "No ingredients listed")
                }
    except requests.exceptions.RequestException:
        pass
    
    # Return placeholder structural values if external API is unreachable or item missing
    return {
        "product_name": "Unknown Product (API Lookup Failed)",
        "brands": "Unknown Brand",
        "ingredients_text": "N/A"
    }


# --- REST API ROUTES ---

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Inventory Management API"}), 200

@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    return jsonify(mock_db), 200


@app.route('/inventory/<barcode>', methods=['GET'])
def get_inventory_item(barcode):
    item = next((x for x in mock_db if x["barcode"] == barcode), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route('/inventory', methods=['POST'])
def add_inventory_item():
    data = request.get_json() or {}
    barcode = data.get("barcode")
    price = data.get("price")
    quantity = data.get("quantity")

    if not barcode or price is None or quantity is None:
        return jsonify({"error": "Missing mandatory fields: barcode, price, quantity"}), 400

    # Ensure uniqueness
    if any(x["barcode"] == barcode for x in mock_db):
        return jsonify({"error": "Product with this barcode already exists"}), 400

    # Enrich internal storage using data from OpenFoodFacts
    api_details = fetch_openfoodfacts_data(barcode)
    
    new_item = {
        "barcode": str(barcode),
        "price": float(price),
        "quantity": int(quantity),
        "status": 1,
        "product": api_details
    }
    
    mock_db.append(new_item)
    return jsonify(new_item), 201


@app.route('/inventory/<barcode>', methods=['PATCH'])
def update_inventory_item(barcode):
    data = request.get_json() or {}
    item = next((x for x in mock_db if x["barcode"] == barcode), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Update only fields provided by client (leaving the rest unchanged)
    if "price" in data:
        item["price"] = float(data["price"])
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])

    return jsonify(item), 200


@app.route('/inventory/<barcode>', methods=['DELETE'])
def delete_inventory_item(barcode):
    global mock_db
    item = next((x for x in mock_db if x["barcode"] == barcode), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404

    mock_db = [x for x in mock_db if x["barcode"] != barcode]
    return '', 204


if __name__ == '__main__':
    app.run(port=5000, debug=True)