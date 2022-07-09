try:
 import unzip_requirements
except ImportError:
 pass
import datetime
from datetime import datetime,date

def convert_date_to_year(document_year):
    date_time = datetime.strptime(document_year, "%m-%d-%Y") # Convert string to datetime
    epoch_time = date_time.timestamp() # Convert datetime to epoch time
    return datetime.fromtimestamp(epoch_time).year # Convert epoch time to datetime object and return the year

def get_document_date(query_answers):
    try:
        return next(x[2] for x in query_answers if x[1] == "DOCUMENT_YEAR")
    except StopIteration:
        return None

def get_year_of_document(query_answers):
    document_date = get_document_date(query_answers)
    year= convert_date_to_year(document_date)
    current_year = date.today().year

    res={"errors":{}}
    res["data"]={
                    "year": year
                }
    if(year==current_year or year==current_year-1 ):
        res["success"]=True
        res["errors"]["expire"]=False
    else:   
        res["success"]=False
        res["errors"]["expire"]=True
    return res
        

    

