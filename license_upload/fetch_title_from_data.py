import requests
from name_matching import query, compare_applicantName_with_title



url = "https://batchdata-property-lookup.p.rapidapi.com/api/v1/property/lookup/all-attributes"

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "607207b6c8mshf455d20b0589775p1384abjsnc103da89952e",
    "X-RapidAPI-Host": "batchdata-property-lookup.p.rapidapi.com"
}


applicant_name = input("Enter applicant name: ")
# street = input("Enter street: ")
# city = input("Enter city: ")
# state = input("Enter state: ")
# _zip = input("Enter zip: ")
street = "851 osmond lane"
city = "provo"
state = "UT"
_zip = "84604"

payload = {"requests": [{"address": {
				"street": street,
				"city": city,
				"state": state,
				"zip": _zip
			}}]}


def getTitleOwner(url, payload, headers):
    response = requests.request("POST", url, json=payload, headers=headers)
    owner_fullName = response.json()['results']['properties'][0]['owner']['names']
    # print(owner_fullName)
    owners = [name for name in owner_fullName]
    return owners

owner_fullName = getTitleOwner(url, payload, headers)
for name in owner_fullName:
    print("name",name)
    compare_applicantName_with_title(query, name['full'], applicant_name)