import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_read_first_chunk(self):
        response = self.client.get("/read/first-chunk")
        self.assertEqual(response.status_code, 200)
        actual_data = response.get_json()
        actual_data_first_two = actual_data[:2]
        expected_data_first_two = [
            {"name": "Fer à boucler Easy Waves Babyliss C260E", "price": 5804.0},
            {"name": "BaByliss Lisseur vapeur I PRO 230 ST395E", "price": 16793.0}
        ]
        self.assertEqual(actual_data_first_two, expected_data_first_two)

if __name__ == '__main__':
    unittest.main()
