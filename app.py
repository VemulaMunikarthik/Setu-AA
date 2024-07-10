from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
client_id = "255d0b6c-492d-44cf-8581-e9494c7b0914"
client_secret = "9c2fc756-3d17-46d6-b28d-be4d71953e83"
api_url = "https://fiu-uat.setu.co"
product_instance_id = "57bddd40-9a18-4bbe-a827-d349992a0647"
redirect_url = "http://localhost:3000/"

# Local storage simulation
local_storage = {}

# Utility functions
def create_data(mobile_number):
    date_now = datetime.utcnow()
    expiry = date_now + timedelta(minutes=10)
    consent_payload = {
        "Detail": {
            "consentStart": date_now.isoformat() + "Z",
            "consentExpiry": expiry.isoformat() + "Z",
            "Customer": {
                "id": f"{mobile_number}@onemoney"
            },
            "FIDataRange": {
                "from": "2021-04-01T00:00:00Z",
                "to": "2021-10-01T00:00:00Z"
            },
            "consentMode": "STORE",
            "consentTypes": ["TRANSACTIONS", "PROFILE", "SUMMARY"],
            "fetchType": "PERIODIC",
            "Frequency": {
                "value": 30,
                "unit": "MONTH"
            },
            "DataFilter": [
                {
                    "type": "TRANSACTIONAMOUNT",
                    "value": "5000",
                    "operator": ">="
                }
            ],
            "DataLife": {
                "value": 1,
                "unit": "MONTH"
            },
            "DataConsumer": {
                "id": "setu-fiu-id"
            },
            "Purpose": {
                "Category": {
                    "type": "string"
                },
                "code": "101",
                "text": "Loan underwriting",
                "refUri": "https://api.rebit.org.in/aa/purpose/101.xml"
            },
            "fiTypes": ["DEPOSIT"]
        },
        "redirectUrl": redirect_url
    }
    return consent_payload

@app.route("/")
def home():
    return "Hello"

@app.route("/consent/<mobile_number>", methods=["GET"])
def create_consent(mobile_number):
    local_storage["consent"] = "Pending"
    body = create_data(mobile_number)
    request_config = {
        "method": "post",
        "url": f"{api_url}/consents",
        "headers": {
            "Content-Type": "application/json",
            "x-client-id": client_id,
            "x-client-secret": client_secret,
            "x-product-instance-id": product_instance_id
        },
        "json": body
    }

    response = requests.request(**request_config)
    if response.status_code == 200:  # Consent creation might return 200 OK
        response_data = response.json()
        consent_id = response_data.get("id")
        consent_url = response_data.get("url")
        local_storage["consent_id"] = consent_id
        return jsonify({"consent_id": consent_id, "url": consent_url})
    else:
        return f" {response.text}", response.status_code

@app.route("/consent-status", methods=["GET"])
def fetch_consent_status():
    consent_request_id = local_storage.get("consent_id")
    if not consent_request_id:
        return "No consent ID found", 400

    request_config = {
        "method": "get",
        "url": f"{api_url}/v2/consents/{consent_request_id}/fetch/status",
        "headers": {
            "x-product-instance-id": product_instance_id,
            "Authorization": f"Bearer {client_secret}"
        }
    }

    response = requests.request(**request_config)
    if response.status_code == 200:
        return response.json()
    else:
        return f"{response.text}", response.status_code

if __name__ == "__main__":
    app.run(port=3000)
