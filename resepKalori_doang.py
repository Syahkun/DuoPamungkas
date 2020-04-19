import requests, json

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"

querystring = {"targetCalories":"2000","timeFrame":"day"}

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(json.dumps(response.json(), indent=2))
