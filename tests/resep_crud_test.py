import json
from . import app, client, cache, create_token, init_database
from unittest import mock
from unittest.mock import patch

class TestResepCrud():

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data

        if len(args) > 0:
            if args[0] == "https://"+ app.config['X_RAPIDAPI_HOST_2'] + "/recipes/mealplans/generate":
                return MockResponse({
                    "meals": [{
                        "id": 201020,
                        "imageType": "jpg",
                        "title": "Breakfast Banh Mi",
                        "readyInMinutes": 80,
                        "servings": 1,
                        "sourceUrl": "http://www.seriouseats.com/recipes/2011/04/breakfast-banh-mi-recipe.html"
                    },
                    {
                        "id": 411153,
                        "imageType": "jpg",
                        "title": "BBQ Chicken Polenta with Fried Egg",
                        "readyInMinutes": 25,
                        "servings": 4,
                        "sourceUrl": "http://www.tasteofhome.com/Recipes/bbq-chicken-polenta-with-fried-egg"
                    },
                    {
                        "id": 643980,
                        "imageType": "jpg",
                        "title": "Fruit Glazed Corned Beef",
                        "readyInMinutes": 45,
                        "servings": 5,
                        "sourceUrl": "https://spoonacular.com/fruit-glazed-corned-beef-643980"
                    }],
                    "nutrients": {
                    "calories": 2785.1,
                    "protein": 129.89,
                    "fat": 141.73,
                    "carbohydrates": 240.69}}, 200)

        else:
            return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_resep_id(self, get_mock, client):
        token = create_token()
        res = client.get(
            '/resep/1', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200