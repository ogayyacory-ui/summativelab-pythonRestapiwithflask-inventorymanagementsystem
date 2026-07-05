import unittest
from unittest.mock import patch

import app as app_module


class InventoryApiTests(unittest.TestCase):
    def setUp(self):
        app_module.mock_db = [
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
            }
        ]
        self.client = app_module.app.test_client()

    def test_get_all_inventory_returns_status_ok(self):
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_single_item_returns_item_when_found(self):
        response = self.client.get("/inventory/008000000661")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["barcode"], "008000000661")

    def test_get_single_item_returns_404_when_missing(self):
        response = self.client.get("/inventory/999999999999")
        self.assertEqual(response.status_code, 404)

    @patch.object(app_module, "fetch_openfoodfacts_data", return_value={
        "product_name": "Test Product",
        "brands": "Test Brand",
        "ingredients_text": "Test ingredients"
    })
    def test_post_creates_new_inventory_item(self, mock_fetch):
        response = self.client.post(
            "/inventory",
            json={"barcode": "123456789012", "price": 2.5, "quantity": 10}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["barcode"], "123456789012")
        self.assertEqual(data["price"], 2.5)
        self.assertEqual(data["quantity"], 10)
        mock_fetch.assert_called_once_with("123456789012")

    def test_patch_updates_existing_item(self):
        response = self.client.patch(
            "/inventory/008000000661",
            json={"price": 4.49, "quantity": 50}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["price"], 4.49)
        self.assertEqual(data["quantity"], 50)

    def test_delete_removes_existing_item(self):
        response = self.client.delete("/inventory/008000000661")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(app_module.mock_db, [])


if __name__ == "__main__":
    unittest.main()
