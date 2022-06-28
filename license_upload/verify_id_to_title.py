import requests
import boto3
import datetime
from textractcaller import call_textract_analyzeid
from name_matching import query, compare_applicantName_with_title
def analyze_ID(document_pages):
    textract_client = boto3.client('textract', region_name='us-east-1')
    license_fields = call_textract_analyzeid(document_pages=document_pages,
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

def getTitleOwner(url, payload, headers):
    owner_fullName = requests.request("POST", url, json=payload, headers=headers).json()['results']['properties'][0]['owner']['names']
    return [name for name in owner_fullName]

def check_license_expiration(license_expiration_date):
    license_expiration_date = license_expiration_date.split('/')
    license_expiration_date = datetime.date(int(license_expiration_date[2]), int(license_expiration_date[0]), int(license_expiration_date[1]))
    today = datetime.date.today()
    if license_expiration_date < today:
        print("License is expired")
        return True
    else:
        print("License is not expired")
        return False

def compare_applicantName_with_title(query, title, applicant_name):
    query = query.replace('$title', f'{title} {title}')
    query = query.replace('$applicant_name', f'{applicant_name} {applicant_name}')
    return query

def isOwner(title_owners):
    return title_owners[0] or title_owners[1]

def main(document_pages):
    payload, applicant_name, license_expiration_date = analyze_ID(document_pages)
    check_license_expiration(license_expiration_date)
    names_that_appear_on_title = getTitleOwner(url, payload, headers)
    title_owners = [(compare_applicantName_with_title(query, name['full'], applicant_name)) for name in names_that_appear_on_title]
    return isOwner(title_owners)

if __name__ == "__main__":
    main(document_pages=['s3://enium-drivers-license-images/enium_test_11.png'])