import requests
from config import API_KEY, CLASSIFICATION_URL, OBJECT_URL


# Get all classifications with >2500 records

def get_classifications():

    params = {
        "apikey": API_KEY,
        "size": 100
    }

    response = requests.get(CLASSIFICATION_URL, params=params)

    data = response.json()

    classifications = []

    for record in data["records"]:

        if record["objectcount"] >= 2500:
            classifications.append(record["name"])

    return classifications


# Download records for selected classification

def collect_data(classification):

    params = {
        "apikey": API_KEY,
        "size": 100,
        "classification": classification
    }

    all_records = []

    for page in range(1, 26):

        params["page"] = page

        response = requests.get(OBJECT_URL, params=params)

        data = response.json()

        records = data["records"]

        if len(records) == 0:
            break

        all_records.extend(records)

    return all_records