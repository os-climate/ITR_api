import requests
import json

url = "http://localhost:8080/temperature_score"

payload = json.dumps({
    "aggregate": True,
    "aggregation_method": "WATS",
    "data_providers": [
        "Excel"
    ],
    "scopes": [
        "S1+S2"
    ],
    "time_frames": [
        "long"
    ],
    "include_columns": [],
    "grouping_columns": [],
    "default_score": 3.2,
    "companies": [
        {
            "company_name": "Company A",
            "company_id": "JP0000000001",
            "company_isin": "JP0000000001",
            "investment_value": 35000000
        },
        {
            "company_name": "Company B",
            "company_id": "NL0000000002",
            "company_isin": "NL0000000002",
            "investment_value": 10000000
        },
        {
            "company_name": "Company C",
            "company_id": "IT0000000003",
            "company_isin": "IT0000000003",
            "investment_value": 10000000
        }
    ],
    "anonymize_data_dump": False
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
