import requests

response = requests.post("http://localhost:5000/api/lookup", json={
    "platform": "ATL",
    "sap": "1114"  # or replace with any valid SAP or UPC
})

print("Status:", response.status_code)
print("Response:", response.json())


