"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
import requests
import json

requests.packages.urllib3.disable_warnings() #Supress SSL verify warnings
response = requests.models.Response #python typing

class urlRequests():
    def __init__(self):
        super().__init__()

    def urlRequest(self, method: str, url: str, data: str=None) -> bytes:      
        """Handles all the URL requests

        Args:
            method (str): HTTP definition type i.e GET,PUT,POST,DELETE
            url (str): Apstra resource URL
            data (str, optional): JSON body of request. Defaults to None:str.

        Raises:
            SystemExit: On failure

        Returns:
            bytes: Request response object
        """ 

        try:
            if self.apiToken == None:
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache" }
                data = '{ \"username\":\"' + self.username + '\", \"password\":\"' + self.password + '\" }'
                response = requests.request(f"{method}", url, data=data, headers=headers, verify=False, timeout=10) 
                if response.raise_for_status() == False:
                    raise requests.exceptions.RequestException
                
            elif method == 'GET':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("GET", url, data=data, headers=headers, verify=False, timeout=10) 
            
            elif method == 'DELETE':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("DELETE", url, data=data, headers=headers, verify=False, timeout=10) 

            elif method == 'POST':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("POST", url, data=data, headers=headers, verify=False, timeout=10) 

            elif method == 'PUT':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("PUT", url, data=data, headers=headers, verify=False, timeout=10) 

            elif method == 'PATCH':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("PATCH", url, data=data, headers=headers, verify=False, timeout=10)

            return response
        except requests.exceptions.RequestException as e:
            self.customError(response=str(e))
            exit(1)
        except requests.exceptions.Timeout as e:
            self.customError(response=str(e))
            exit(1)