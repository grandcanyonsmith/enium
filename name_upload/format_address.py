import requests
import json
def format_address(address):
    url = "https://address-completion.p.rapidapi.com/v1/geocode/autocomplete"

    querystring = {"text":address,"limit":"1","lang":"en"}

    headers = {
        "X-RapidAPI-Key": "607207b6c8mshf455d20b0589775p1384abjsnc103da89952e",
        "X-RapidAPI-Host": "address-completion.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()['features'][0]['properties']
    
    street_address = response['address_line1']
    city = response['city']
    state = response['state_code']
    zip_ = response['postcode']
    
    return(street_address,city,state,zip_)

