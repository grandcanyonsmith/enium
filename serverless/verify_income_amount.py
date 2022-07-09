try:
 import unzip_requirements
except ImportError:
 pass
import boto3
import datetime
# from verify_date_of_document import get_year_of_document
import sys
from tabulate import tabulate
import trp.trp2 as t2
from verify_date_of_document import *
from verify_income_amount import *
from verify_name_on_document import *
import json
import pdf2image
import requests

def verify_income(reported_income, query_answers):
    res={"errors":{}}
    for x in query_answers:
        if x[1] == "PAYSTUB_CURRENT_GROSS":
            current_gross = x[2]

            current_gross = float(current_gross.replace("$", "")
                                  .replace(",", ""))
            current_gross *= 24

            if current_gross < reported_income:
                res["success"]=False
                res["errors"]["income"]=True
                res["data"]={
                    "income":current_gross
                }
                print("Income is incorrect")
                print(f"Current gross pay: ${current_gross}")
                print(f"Reported income: ${reported_income}")
                return res
            else:
                res["success"]=True
                res["errors"]["income"]=False
                res["data"]={
                    "income":current_gross
                }
                print("Income is correct")
                print("Current gross pay: $" + str(current_gross))
                print("Reported income: $" + str(reported_income))
                return res


def handler(event, context):
    body = json.loads(event["body"])

    reported_income = int(body["income"])
    document=body["document"]

    res={}

    textract = boto3.client('textract', region_name='us-east-1')
    try:
        docObj=None;
        if document.split(".")[-1]=="pdf":
            pdf = requests.get('https://asce4s-test-id-bucket.s3.amazonaws.com/'+document, stream=True)
            images=pdf2image.convert_from_bytes(pdf.raw.read())

            images[0].save('/tmp/output.jpg', 'JPEG')
            document= open('/tmp/output.jpg', 'rb') 
            imageBytes = bytearray(document.read())
            docObj={'Bytes': imageBytes}
        else:
            docObj={'S3Object': {'Bucket': 'asce4s-test-id-bucket', 'Name': document}}




        response = textract.analyze_document(
            Document=docObj,
            FeatureTypes=["QUERIES"],
            QueriesConfig={
                "Queries": [{
                    "Text": "What is the year to date gross pay",
                    "Alias": "PAYSTUB_YTD_GROSS"
                },
                {
                    "Text": "What is the current gross pay?",
                    "Alias": "PAYSTUB_CURRENT_GROSS"
                },
                {
                    "Text": "What is the current net pay?",
                    "Alias": "PAYSTUB_CURRENT_NET"
                },
                {   "Text": "Date of document?",
                    "Alias": "DOCUMENT_YEAR"
                },
                {
                    "Text": "What is the owner address?",
                    "Alias": "OWNER_ADDRESS"
                    },
                {
                    "Text": "What is the owner name?",
                    "Alias": "OWNER_NAME"
                    }]
            })




        d = t2.TDocumentSchema().load(response)
        page = d.pages[0]

        query_answers = d.get_query_answers(page=page)

        res={}

        income_res=verify_income(reported_income, query_answers)
        name_res=verify_name(body["name"], query_answers)
        year_res=get_year_of_document(query_answers)

        if income_res["success"] and name_res["success"] and income_res["success"]:
            res["success"]=True
            res["message"]="Income Verification Success"
        else:
            res["success"]=False
            res["message"]="Income Verification Failed"
            
        res["data"]={**income_res["data"], **name_res["data"], **year_res["data"]}
        res["errors"]={**income_res["errors"], **name_res["errors"], **year_res["errors"]}
   
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(res)
        }

        return response

    except:
        res={}
        res["success"]=False
        res["message"]="Image processing failed"
        response = {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(res)
        }
        return response

