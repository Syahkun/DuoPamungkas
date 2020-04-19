import requests, json

## inputan awal
berat = 40
tinggi = 1.60
age = 23
gender = 'M' ## pilihan M (Male) or F (Female)

## Max 1000 per bulan (API: Health)
url = "https://gabamnml-health-v1.p.rapidapi.com/bmi"

querystring = {"weight": berat,"height": tinggi}

headers = {
    'x-rapidapi-host': "gabamnml-health-v1.p.rapidapi.com",
    'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
status = response.json()['status']

## Mau masuk ke API 2
if gender == "M":
    BMR = 66 + (13.86*berat) + (5.03*tinggi) - (6.8*age)
else:
    BMR = 655 + (9.46*berat) + (1.83*tinggi) - (4.7*age)

if status == "Overweight":
    BMR *= 0.6
elif status == "Low":
    BMR *= 1.8
elif status == "Normal":
    BMR *= 1.2


## Max 500 per hari (API: Recipe-Food-Nutrition)
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"

querystring = {"targetCalories": BMR,"timeFrame":"day"}

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(json.dumps(response.json(), indent=2))



