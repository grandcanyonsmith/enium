try:
 import unzip_requirements
except ImportError:
 pass
import requests
import boto3
from textractcaller import call_textract_analyzeid
from name_matching import query, compare_applicantName_with_title
import json
import datetime

url = "https://batchdata-property-lookup.p.rapidapi.com/api/v1/property/lookup/all-attributes"

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "607207b6c8mshf455d20b0589775p1384abjsnc103da89952e",
    "X-RapidAPI-Host": "batchdata-property-lookup.p.rapidapi.com"
}


def analyze_ID(image):
    textract_client = boto3.client('textract', region_name='us-east-1')
    license_fields = call_textract_analyzeid(document_pages=["s3://asce4s-test-id-bucket/"+image],
                                boto3_textract_client=textract_client)['IdentityDocuments'][0]['IdentityDocumentFields']
    '''
    Name on license
    '''

    print(license_fields
    )
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

def getTitleOwner(url, payload, headers):
    response = requests.request("POST", url, json=payload, headers=headers)
    
    owner_fullName = response.json()['results']['properties'][0]['owner']['names']
    return [name for name in owner_fullName]


    


def handler(event, context):
    body = json.loads(event["body"])
    payload, applicant_name, license_expiration_date = analyze_ID(body["image"])
    print(applicant_name)
    res={}
    
    
    if applicant_name.strip() =="":
        res={
            "success":False,
            "message":"Application Failed",
            "errors":{
                "blurred" :True,
                "cropped":False
            }
        }
    else:
       
        expired= check_license_expiration(license_expiration_date)
        res=compare_applicantName_with_title(query, body["name"], applicant_name)

        if expired:
            res["success"]=False
            res["message"]="Application Failed"
            res["errors"]["expired"]=True
        else:
            res["errors"]["expired"]=False

        res["errors"][ "blurred"]=False
        res["errors"][ "cropped"]=False
            
    res["data"]={
        "license_name":applicant_name,
        "address_name": body["name"],
        "license_expiration_date":license_expiration_date
    }
    
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
         },
        "body": json.dumps(res)
    }

    return response


# {'status': {'code': 200, 'text': 'OK'}, 'results': {'properties': [{'_id': '91eb7deb3cc32b5259ce2e4415cd08b3', 'address': {'oldHashes': ['4b9b01be439338b077317b12f6110ddb'], 'houseNumber': '3120', 'street': '3120 Foothill Blvd', 'city': 'Oroville', 'county': 'Butte', 'state': 'CA', 'zip': '95966', 'zipPlus4': '6811', 'localities': ['oroville'], 'hash': '4b9b01be439338b077317b12f6110ddb', 'latitude': 39.4865369544998, 'longitude': -121.509210556585, 'normalized': True, 'countyFipsCode': '06007', 'formattedStreet': 'Foothill Blvd', 'streetNoUnit': '3120 Foothill Blvd', 'geoStatusCode': 'B', 'geoStatus': 'Rooftop'}, 'assessment': {'assessedImprovementValue': 92959, 'assessedLandValue': 82023, 'totalAssessedValue': 174982, 'assessmentYear': 2021}, 'building': {'totalBuildingAreaSquareFeet': 1352, 'totalBuildingAreaCode': 'L', 'totalBuildingAreaCodeDescription': 'Living Area', 'garageSquareFeet': 1440, 'garageUnfinishedSquareFeet': 0, 'garageFinishedSquareFeet': 0, 'yearBuilt': 1997, 'effectiveYearBuilt': 1997, 'roomCount': 4, 'unitCount': 1, 'bedroomCount': 2, 'calculatedBathroomCount': 2, 'fullBathroomCount': 2, 'bathroomCount': 2, 'garageParkingSpaceCount': 5, 'features': ['Air Conditioning', 'Garage', 'Attached Garage', 'Central Air Conditioning'], 'airConditioningSourceCode': '1', 'airConditioningSource': 'Central', 'buildingQualityCode': '4', 'buildingQuality': 'B', 'garageCode': '1', 'garage': 'Attached Garage', 'heatSourceCode': '3', 'heatSource': 'Central', 'styleCode': '33', 'style': 'Mobile Home'}, 'demographics': {'age': 64, 'householdSize': 3, 'income': 45800, 'netWorth': 75000, 'discretionaryIncome': 7500, 'homeownerRenterCode': 'R', 'homeownerRenter': 'Renter', 'genderCode': 'F', 'gender': 'Female', 'childCount': 1, 'hasChildren': True, 'investments': ['Personal'], 'maritalStatusCode': 'S', 'maritalStatus': 'Single', 'petOwner': True, 'singleParent': True, 'religious': True, 'religiousAffiliationCode': 'C', 'religiousAffiliation': 'Catholic', 'householdEducationCode': '2', 'householdEducation': 'Completed College', 'individualEducationCode': '2', 'individualEducation': 'Completed College', 'householdOccupationCode': '2', 'individualOccupationCode': '2'}, 'foreclosure': {}, 'general': {'primaryParcel': True, 'parcelCount': 1, 'vacant': False, 'mailingAddressVacant': False, 'standardizedLandUseCode': '1006', 'propertyTypeCategory': 'Residential', 'propertyTypeDetail': 'Mobile/Manufactured Home', 'congressionalDistrict': '01', 'timeZone': 'Pacific', 'utcOffset': -8, 'daylightSavingsTime': True, 'carrierRoute': 'C015', 'censusTract': '003100', 'schoolDistrict': 'Oroville City Elementary School District'}, 'ids': {'addressHash': '4b9b01be439338b077317b12f6110ddb', 'apn': '078-340-036-000', 'quantariumUrn': '9903928', 'fipsCode': '06007', 'personIds': []}, 'involuntaryLien': {'bankruptcy': {}, 'divorce': {}, 'liens': []}, 'legal': {'legalDescription': '3120 FOOTHILL BLVD', 'subdivisionName': 'OROVILLE WYANDOTTE FRUIT LANDS', 'tractNumber': 'OROVILLE WYANDOTTE FRUIT LANDS'}, 'lot': {'lotSizeAcres': 1.77, 'lotDepthFeet': 0, 'lotSizeSquareFeet': 77101, 'zoningCode': 'MDR', 'estimatedLotSizeSquareFeet': 70691}, 'mls': {'brokerage': {}}, 'openLien': {}, 'owner': {'fullName': 'Ryan Karen Revocable Living Trust', 'mailingAddress': {'oldHashes': [], 'houseNumber': '3120', 'street': '3120 Foothill Blvd', 'city': 'Oroville', 'county': 'Butte', 'state': 'CA', 'zip': '95966', 'formattedStreet': 'Foothill Blvd', 'streetNoUnit': '3120 Foothill Blvd', 'hash': '4b9b01be439338b077317b12f6110ddb'}, 'names': [{'first': 'Ryan Karen Revocable Living Trust', 'full': 'Ryan Karen Revocable Living Trust'}], 'ownerOccupied': True, 'ownerStatusType': 'Company Owned', 'ownershipRightsCode': 'RT', 'ownershipRights': 'Revocable Trust'}, 'quickLists': {'absenteeOwner': False, 'absenteeOwnerInState': False, 'absenteeOwnerOutOfState': False, 'activeListing': False, 'activeAuction': False, 'bankruptcy': False, 'cashBuyer': False, 'corporateOwned': True, 'divorce': False, 'expiredListing': False, 'freeAndClear': True, 'highEquity': True, 'inherited': False, 'liens': False, 'listedBelowMarketPrice': False, 'lowEquity': False, 'mailingAddressVacant': False, 'noticeOfDefault': False, 'onMarket': False, 'outOfStateOwner': False, 'ownerOccupied': True, 'pendingListing': False, 'preforeclosure': False, 'recentlySold': False, 'samePropertyAndMailingAddress': True, 'taxDefault': False, 'tiredLandlord': False, 'unknownEquity': False, 'vacant': False, 'hasHoaFees': False}, 'sale': {'lastTransfer': {'saleBuyers': [], 'saleSellers': []}, 'lastSale': {'saleBuyers': [], 'saleSellers': []}, 'priorTransfer': {'saleBuyers': [], 'saleSellers': []}, 'priorSale': {'saleBuyers': [], 'saleSellers': []}}, 'tax': {'taxAmount': 1850.64, 'taxYear': 2021, 'taxRateCodeArea': '91-001', 'taxExemptions': ['Homestead']}, 'valuation': {'estimatedValue': 322184.10000000003, 'priceRangeMin': 163097, 'priceRangeMax': 450586, 'standardDeviation': 0.4684, 'confidenceScore': 6, 'asOfDate': '2021-10-06T00:00:00.000Z', 'equityCurrentEstimatedBalance': 322184, 'equityPercent': 100}, 'meta': {'importEvents': [], 'requestId': 'wqmPggZWhO'}, 'homeownerAssociations': []}], 'meta': {'apiVersion': '2.14.1', 'performance': {'totalRequestTime': 595, 'startTime': '2022-06-14T21:38:26.924Z', 'endTime': '2022-06-14T21:38:27.519Z'}, 'results': {'requestCount': 1, 'matchCount': 1, 'noMatchCount': 0, 'errorCount': 0}, 'requestId': 'U3mapzBjffPOrYP'}}}