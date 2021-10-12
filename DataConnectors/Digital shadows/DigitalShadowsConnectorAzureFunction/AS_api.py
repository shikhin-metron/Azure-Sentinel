""" handles all Azure sentinel apis related functions here """
import base64
import datetime
import requests
import hmac
import hashlib
from requests.models import CaseInsensitiveDict

class logs_api:
    """ 
    class for log analytics api 
    """
    
    def __init__(self, id, key):                            
        """ 
            constructor initializing azure creds.
            id is workspace id and key is primary key
        """
        
        self.customer_id = id
        self.shared_key = key

    
    def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
        """ 
            Build the API signature
        """
        
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, encoding="utf-8")  
        decoded_key = base64.b64decode(shared_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
        authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
        return authorization
    
    def post_data(self, body, log_type):
        """ 
            Build and send a request to the POST API 
        """
        
        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        signature = logs_api.build_signature(self.customer_id, self.shared_key, rfc1123date, content_length, method, content_type, resource)
        uri = 'https://' + self.customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': log_type,
            'x-ms-date': rfc1123date
        }

        response = requests.post(uri,data=body, headers=headers)
        print(response.text)
        if (response.status_code >= 200 and response.status_code <= 299):
            print('Accepted')
        else:
            print("Response code: {}".format(response.status_code))


            
class management_api:
    """ class for api modifiying and getting the data in incidents section of azure sentinel using management api """
    def __init__(self):
        """
            initialize all the creds of azure management api here 
        """

        self.subsciptionID = "9ecebafb-a962-4e36-9e10-0cfbbc18b52f"
        self.resourceGroup = "digitalshadows"
        self.workspaceName = "DigitalShadowsResearch"
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtpZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9mMGJhOGM2ZC02NDI1LTQ1ODktODBmZi1hZDQ4ODQ5NzFkYWQvIiwiaWF0IjoxNjMzOTQ5OTA5LCJuYmYiOjE2MzM5NDk5MDksImV4cCI6MTYzMzk1MzgwOSwiYWNyIjoiMSIsImFpbyI6IkFVUUF1LzhUQUFBQXBYdno3bGdkeFl0WGdXWEZnVHZRZWhwS3hpRy9rWkszVnhlOFJYemorTmVOVVd4NU1nN2diL3kyUUQvMlY5NW9DUHBIOVlHQk9GQkdScEFnbStPMUN3PT0iLCJhbXIiOlsicHdkIiwibWZhIl0sImFwcGlkIjoiMDRiMDc3OTUtOGRkYi00NjFhLWJiZWUtMDJmOWUxYmY3YjQ2IiwiYXBwaWRhY3IiOiIwIiwiZ3JvdXBzIjpbIjM2ZDYwZDYzLTEwOTYtNGRkMy1iZGJjLTg3MzU2N2U5ZDU3YSJdLCJpcGFkZHIiOiIxMDMuMTA2LjEwMS4yMDIiLCJuYW1lIjoiU2hpa2hpbiBEYWhpa2FyIiwib2lkIjoiNWFlMGZmZWUtNmU2Zi00ZDQ0LWI0NDgtMTBlZmU3ZTUyOTdhIiwicHVpZCI6IjEwMDMyMDAxNkRENDUzM0IiLCJyaCI6IjAuQVhBQWJZeTY4Q1ZraVVXQV82MUloSmNkclpWM3NBVGJqUnBHdS00Qy1lR19lMFp3QUlJLiIsInNjcCI6InVzZXJfaW1wZXJzb25hdGlvbiIsInN1YiI6IjFMaUgtSzVhdEhkMjV2SzA1S0M2S1IyeXhQc0RncVJFM0lVRWlOS0ZaN0kiLCJ0aWQiOiJmMGJhOGM2ZC02NDI1LTQ1ODktODBmZi1hZDQ4ODQ5NzFkYWQiLCJ1bmlxdWVfbmFtZSI6InNoaWtoaW5AbWV0cm9ubGFicy5jb20iLCJ1cG4iOiJzaGlraGluQG1ldHJvbmxhYnMuY29tIiwidXRpIjoidjI3blhBSTc5VS1pVVA1MVNRNEhBUSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc190Y2R0IjoxNjI1NzIzNjUwfQ.g67C2dQEz5i5H6oyqCICN4fsuus_B6CTrBKUjxjqfL6EKlFNCFK-GPQivb_OyjgZc5kFc9uwOaGUlBkQtjujVj1IQ3bU1tM8QTztok1uSOc75_wjyy2wLxXl3WdtTD7PslhH3J1pMOrDeG9zSnOXZbtO5bOG8LXFvpRx7RZ3xhJ0a-n0WwvOLsAzC6Efcel_EKElK0nEyidyXBFFAKtsiozxF8uKnQxejRcA9P6Dm9h2MbVwtX6UyEiKnPDvKtS1m2lpV_TNQ87zfaYSUpmc55c64qGIWiLNSMyGWF2ykMgGf3r8o_KTZH8yvEEt9zX7yE4Stwu5OD4qdVCutKt_bQ"
        
        self.user = "shikhin@metronlabs.com"
        self.passwd = "RGwHdasxg6Xhk3a"


    def get_azure_incidents(self):
        url = "https://management.azure.com/subscriptions/" + self.subsciptionID + "/resourceGroups/" + self.resourceGroup + "/providers/Microsoft.OperationalInsights/workspaces/" + self.workspaceName + "/providers/Microsoft.SecurityInsights/incidents?api-version=2021-04-01"
        
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + self.token

        response = requests.get(url, headers=headers)

        data = response.json
        return data