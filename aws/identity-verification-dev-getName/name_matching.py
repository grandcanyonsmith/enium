try:
 import unzip_requirements
except ImportError:
 pass

"""
This file contains the functions to query the API and compare the applicant name with the title.
It uses a machine learning 'Natural Language Processing' model created by Facebook called Bart to compare the applicant name with the title.
Using this model, it can match names to predict a likelihood that a solar customer name is the same as the title.
As a rule of thumb, anything above 95% match is a pass.
"""

from numpy import full
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer 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"}

"""Query the API with the payload and return the response."""
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


"""Compare the applicant name with the title and return the confidence score."""
def compare_applicantName_with_title(query, applicant_name,full_name):
    _input = f"Home Owner: " + applicant_name
    output = query({
    "inputs": [_input],
    "parameters": {"candidate_labels": ["Home Owner: " + full_name]},
    })

    confidence_score = float(output[0]['scores'][0])

    res={}

    if confidence_score > 0.90:
        res["success"]=True
        res["message"] ="Verification Success"
        res["logs"]=[
            "Application Pass",
            "Name in the Drivers License: " + applicant_name,
            "Title Owner's Name: " + full_name,
            "Confidence Score: "+str((confidence_score * 100).__round__(2))+"%"
        ]
        print("Application Pass")
        print(f"\nName in the Drivers License: " + applicant_name)
        # print("Title Owner's Name: " + full_name)
        # make a percentage of the confidence score
        print(f"Confidence Score: {(confidence_score * 100).__round__(2)}%")
        # exit after the first match
        return res

    else:
        res["success"]=False
        res["message"] ="Verification Failed"
        res["logs"]=[
            "Application Fail",
            "Name in the Drivers License: " + full_name,
            "Title Owner's Name: " + applicant_name,
            "Confidence Score: "+ str((confidence_score * 100).__round__(2))+"%"
        ]
        print(f"Application Fail")
        print(f"\nName in the Drivers License: " + full_name)
        print(f"Title Owner's Name: " + applicant_name)
        print(f"Confidence Score: {(confidence_score * 100).__round__(2)}%")
    return res