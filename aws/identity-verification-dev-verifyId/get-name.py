try:
 import unzip_requirements
except ImportError:
 pass
import json
import requests
from name_matching import query,compare_applicantName_with_title

url = "https://batchdata-property-lookup.p.rapidapi.com/api/v1/property/lookup/all-attributes"

headers = {
"content-type": "application/json",
"X-RapidAPI-Key": "607207b6c8mshf455d20b0589775p1384abjsnc103da89952e",
"X-RapidAPI-Host": "batchdata-property-lookup.p.rapidapi.com"
}

def checkParams(key, body):
    if key in body:
        return body[key]
    else:
        return None

def validateRequest(body):
    if checkParams("street",body) is None or checkParams("city",body) is None or checkParams("state",body) is None or  checkParams("zip",body) is None:
        return False
    return True

def getTitleOwner(url, payload, headers):
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.json()['results']['properties'][0]['owner'])
        owner_fullName = response.json()['results']['properties'][0]['owner']['names']
        # print(owner_fullName)
        owners = [name for name in owner_fullName]
        return owners
    except:
        return None



def handler(event, context):
    body = json.loads(event["body"])

    if(validateRequest(body)==False):
        return {
            "statusCode": 400,
        }
    

    

    payload = {"requests": [{"address": {
    "street": body["street"],
    "city": body["city"],
    "state": body["state"],
    "zip": body["zip"]
    }}]}
   
    owner_fullName = getTitleOwner(url, payload, headers)
    body = {
        "name": owner_fullName,
       
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
         },
        "body": json.dumps(body)
    }

    return response
