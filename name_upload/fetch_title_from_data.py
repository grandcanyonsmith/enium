import requests
from name_matching import query, compare_applicantName_with_title
from format_address import format_address

url = "https://batchdata-property-lookup.p.rapidapi.com/api/v1/property/lookup/all-attributes"
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "607207b6c8mshf455d20b0589775p1384abjsnc103da89952e",
    "X-RapidAPI-Host": "batchdata-property-lookup.p.rapidapi.com"
}

street, city, state, _zip = format_address(input("Enter Address: ")) #format_address returns the street, city, state, and zip so that it can be used in the query function of getting title owner

applicant_name = input("Enter Applicant Name: ")

payload = {"requests": [{"address": {
				"street": street,
				"city": city,
				"state": state,
				"zip": _zip
			}}]}


def getTitleOwner(url, payload, headers):
    response = requests.request("POST", url, json=payload, headers=headers)
    r = response.json()['results']['properties'][0]['owner']

    owners = response.json()['results']['properties'][0]['owner']['names']

    try:
        formatted_name = f"{r['names'][0]['first']} {r['names'][0]['middle']} {r['names'][0]['last']}" #if there is a middle name, it will be formatted as first middle last
    except:
        formatted_name = f"{r['names'][0]['first']} {r['names'][0]['last']}" #if there is no middle name, it will be formatted as first last
    
    return owners, formatted_name

owners, formatted_name = getTitleOwner(url, payload, headers)
for person in owners:
    compare_applicantName_with_title(query, person['full'], applicant_name, formatted_name)
