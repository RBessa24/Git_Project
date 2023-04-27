# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-04-16 17:37:45
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-24 09:48:09
import requests
import json

# This is a dummy test!
# This is a dummy test!
def create_organization_test(base_url):
    
    payload = json.dumps({
        "tradingName": "Ritain",
        "isHeadOffice": True,
        "isLegalEntity": True,
        "name": "Ritain - Fundao Headquarters",
        "organizationType": "Company",
        "existsDuring": {
            "startDateTime": "2015-10-22T08:31:52.026Z"
        },
        "status": "validated"
    })
    
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST",
        url=f"{base_url}/organization",
        headers=headers,
        data=payload
    )

    response_data = response.json()
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Response data: {response_data}")
    
    if response.status_code != 201:
        print("Error in creating and organization. Status code: " +
              f"{response.status_code}")
        return False
    if "id" not in response_data:
        return False
    if response_data["name"] != "Ritain - Fundao Headquarters":
        return False
    if response_data["organizationType"] != "Company":
        return False
    if response_data["tradingName"] != "Ritain":
        return False
    
    return True