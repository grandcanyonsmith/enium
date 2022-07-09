# given a name on a document, verify that the name is correct
try:
 import unzip_requirements
except ImportError:
 pass
from verify_income_amount import *


def verify_name(name, query_answers):
    res={"errors":{}}
    for x in query_answers:
        if x[1] == "OWNER_NAME":
            if x[2] == name:
                res["success"]=True
                res["errors"]["name"]=False
                res["data"]={
                    "name":name,
                    "doc_name":x[2]
                }
                print("Name is correct")
                print(f"Name: {x[2]}")
                return res
            else:
                res["success"]=False
                res["errors"]["name"]=True
                res["data"]={
                    "name":name,
                    "doc_name":x[2]
                }
                print("Name is incorrect")
                print(f"Name: {x[2]}")
                return res
