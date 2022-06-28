import requests
import boto3
import datetime
from textractcaller import call_textract_analyzeid
from name_matching import query, compare_applicantName_with_title

url = "https://batchdata-property-lookup.p.rapidapi.com/api/v1/property/lookup/all-attributes"

def analyze_ID():
    textract_client = boto3.client('textract', region_name='us-east-1')
    license_fields = call_textract_analyzeid(document_pages=["s3://enium-drivers-license-images/enium_test_11.png"],
                                boto3_textract_client=textract_client)['IdentityDocuments'][0]['IdentityDocumentFields']
    '''
    Name on license
    '''
    first_name = license_fields[0]['ValueDetection']['Text']
    last_name = license_fields[1]['ValueDetection']['Text']
    applicant_name = f"{first_name} {last_name}"

    '''
    Address on license
    '''
    street = license_fields[17]['ValueDetection']['Text']
    city = license_fields[4]['ValueDetection']['Text']
    state = license_fields[6]['ValueDetection']['Text']
    _zip = license_fields[5]['ValueDetection']['Text']
    expiration_date = license_fields[8]['ValueDetection']['Text']
    '''
    Date that license expires
    '''
    license_expiration_date = license_fields[9]['ValueDetection']['Text']
    '''
    Formatted payload for API call
    '''
    payload = {"requests": [{"address": {
        "street": street,
        "city": city,
        "state": state,
        "zip": _zip
    }}]}
    return payload, applicant_name, license_expiration_date

def check_license_expiration(license_expiration_date: str):
    license_expiration_date = license_expiration_date.split('/')
    license_expiration_date = datetime.date(int(license_expiration_date[2]), int(license_expiration_date[0]),
                                            int(license_expiration_date[1]))
    today = datetime.date.today()
    return license_expiration_date < today

def get_title_owner(url: str, payload, headers):
    owner_fullName = requests.request("POST", url, json=payload, headers=headers).json()['results']['properties'][0]['owner']['names']
    return [name for name in owner_fullName]

def compare_applicant_name_with_title(query: str, full_name: str, applicant_name):
    return query in full_name.lower() or query in applicant_name.lower()

def title_matching(names_that_appear_on_title, applicant_name):
    return [compare_applicant_name_with_title(query, name['full'], applicant_name) for name in names_that_appear_on_title]

if __name__ == "__main__":
    payload, applicant_name, license_expiration_date = analyze_ID()
    if check_license_expiration(license_expiration_date):
        print("License is expired")
    else:
        print("License is not expired")
    names_that_appear_on_title = get_title_owner(url, payload, headers)
    if True in title_matching(names_that_appear_on_title, applicant_name):
        print("Title owners match applicant name")
    else:
        print("Title owners don't match applicant name")