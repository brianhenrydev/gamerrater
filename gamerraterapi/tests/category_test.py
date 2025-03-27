import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer
from rest_framework.authtoken.models import Token


class CategoryTest(APITestCase):
    fixtures = ["token", "users", "categories"]

    def setUp(self):
        pass

    def test_create_category(self):
        url = "/categories"
        data = {"label": "Strat"}

        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["label"], "Strat")
