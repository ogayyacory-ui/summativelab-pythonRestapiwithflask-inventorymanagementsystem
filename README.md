# Inventory Management API

A simple Flask REST API for managing inventory items with CRUD routes and OpenFoodFacts enrichment.

## Features
- View all inventory items
- View a single item by barcode
- Add a new inventory item
- Update price and quantity
- Delete an inventory item
- Enrich product details using the OpenFoodFacts API

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the app
```bash
python app.py
```

The API will be available at http://127.0.0.1:5000/inventory.

## Example requests
### Get all inventory
```bash
curl http://127.0.0.1:5000/inventory
```

### Add an item
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"barcode":"123456789012","price":2.5,"quantity":10}'
```

### Update an item
```bash
curl -X PATCH http://127.0.0.1:5000/inventory/123456789012 \
  -H "Content-Type: application/json" \
  -d '{"quantity":15}'
```

### Delete an item
```bash
curl -X DELETE http://127.0.0.1:5000/inventory/123456789012
```

## Testing
Run the test suite with:
```bash
python -m unittest discover -s tests -v
```
