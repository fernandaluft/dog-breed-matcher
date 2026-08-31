#Project Dog Breed Match

# Imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("DOG_API_KEY")
url="https://api.thedogapi.com/v1/breeds"
headers = {"x-api-key": api_key}

response = requests.get(url, headers=headers)
data = response.json()

clean_data = []

for breed in data:
    clean_data.append({
        "id": breed.get("id"),
        "name": breed.get("name"),
        "life_span": breed.get("life_span"),
        "temperament": breed.get("temperament"),
        "origin": breed.get("origin"),
        "country_code": breed.get("country_code"),
        "breed_group": breed.get("breed_group"),
        "description": breed.get("description"),
        "history": breed.get("history"),
        "weight_metric": breed.get("weight", {}).get("metric"),
        "height_metric": breed.get("height", {}).get("metric"),
        "reference_image_id": breed.get("reference_image_id")
    })

df_raw = pd.DataFrame(clean_data)

# Save raw data
os.makedirs("/app/data/", exist_ok=True)

with open("data/dog_breeds_raw.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Saved {len(data)} breeds.")


