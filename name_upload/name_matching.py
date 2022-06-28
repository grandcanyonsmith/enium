import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def compare_applicantName_with_title(query, name_on_title, full_name, formatted_name):
    _input = f"Home Owner: " + name_on_title  # the text that we want the model to compare and predict

    output = query({
        "inputs": [_input],
        "parameters": {"candidate_labels": ["Home Owner: " + name_on_title]},  # we give the model what it's predicting (a candidate label)
    })
    
    confidence_score = float(output[0]['scores'][0])
    
    if confidence_score > 0.90:
        print("\nName on title: " + name_on_title + f" ({(confidence_score * 100).__round__(2)}% Match)")
        print("\nUpdated application name: " + formatted_name)  # if the confidence score is above 90%, it's a pass
        exit()
        
    else:
        print("\nName on title: " + name_on_title + f" ({(confidence_score * 100).__round__(2)}% Match)")
        print("\nUpdated application name: " + formatted_name)  # if the confidence score is below 90%, it's a fail
        exit()   # exit after the first match
