"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
import requests
import json
    
class login():

    def __init__(self):
        super().__init__() 
    
    
    def login(self, **kwargs: dict) -> None:        
        """Login and get API token + create base URL
        
        Args:
            kwargs (dict): HTTP definition type i.e GET,PUT,POST,DELETE      

        Kwargs:  
            kwargs['password'] (str): AOS password
            kwargs['username'] (str): AOS username
            kwargs['address'] (str): AOS server IP address
            kwargs['port'] (str): AOS port number 
        """        
        
        self.password=kwargs['password']
        self.username=kwargs['username']
        self.address=kwargs['address']
        self.port=str(kwargs['port'])
        self.createBaseUrl()
        response = self.getApiToken()
        self.customSuccess(response=response)
        return response

    def getApiToken(self):
        """Create new API token

        Creates new API token by loging in. The new token is saved as a instance
        varible.
        """        
        loginUrl = self.baseUrl + '/api/user/login'
        self.apiToken = None
        response = self.urlRequest(url=loginUrl, method='POST')
        self.apiToken = response.json()['token']
        return response
        
    def createBaseUrl(self):
        """Create the base URL

        Creates the base URL using the address and port number. This is used by 
        every other instance
        """        
        self.baseUrl = 'https://' + self.address + ':' + self.port 