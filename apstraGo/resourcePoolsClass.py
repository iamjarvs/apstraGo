"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
import requests
import json
 
class resourcePools():

    def __init__(self):
        super().__init__() 


    """
    ASN Pools
    """
    def resourceAsnCreate(self, poolName: str, firstAsn: int, lastAsn: int) -> bytes:
        """This method is used to create ASN pools

        Args:
            poolName (str): Name of the ASN pool to be created
            firstAsn (int): First ASN number in the pool
            lastAsn (int): Last ASN number in the pool

        Returns:
            bytes: Request response object
        """
        url = self.baseUrl + self.urlAsnPool
        data = f''' {{ "display_name": "{poolName}",
                        "id": "{poolName}",
                        "ranges": [
                            {{
                            "first": "{firstAsn}",
                            "last": "{lastAsn}"
                            }}
                        ]
                    }}'''

         
        response = self.urlRequest(url=url, method='POST', data=data)
        return response

    def resourceAsnDelete(self, poolName: str) -> bytes:
        """Used to delete ASN pools via the resourse ID

        Args:
            poolName (str): ID of the pool you want to delete

        Returns:
            response: Request response object
        """        
        if poolName != '':
            url = self.baseUrl + self.urlAsnPool + '/' + poolName
            response = self.urlRequest(url=url, method='DELETE')
            return response

    def resourceAsnGet(self) -> dict:
        """Pulls information on all pools

        Returns:
            dict: dict of all ANS pools configured
        """
        url = self.baseUrl + self.urlAsnPool
        response = self.urlRequest(url=url, method='GET')
        returnedDic = response.json()
        returnedDic['totalPoolCount'] = len(returnedDic['items'])
        return returnedDic


    """
    IP Pools
    """
    def resourceIpCreate(self, poolName: str, network: str) -> bytes:
        """This method is used to create IP pools

        Args:
            poolName (str): Name of the IP pool to be created
            network (str): IP subnet i.e 192.168.1.0/24

        Returns:
            bytes: Request response object
        """        
        
        url = self.baseUrl + self.urlIpPool

        data = f''' {{             
                        "subnets": [ {{"network": "{network}"}} ],
                        "display_name": "{poolName}",
                        "id": "{poolName}"
                    }}'''

         
        response = self.urlRequest(url=url, method='POST', data=data)
        return response

    def resourceIpDelete(self, poolName: str) -> bytes:
        """Used to delete IP pools via the resourse ID

        Args:
            poolName ([type]): Name of pool to be deleted

        Returns:
            bytes: Request response 
        """
        if poolName != '':
            url = self.baseUrl + self.urlIpPool + '/' + poolName
            response = self.urlRequest(url=url, method='DELETE')
            return response

    def resourceIpGet(self) -> bytes:
        """Pulls information on all pools

        Returns:
            bytes: Request response 
        """        
        url = self.baseUrl + self.urlIpPool
        response = self.urlRequest(url=url, method='GET')
        return response


    """
    VNI Pools
    """
    def resourceVniCreate(self, poolName: str, firstVni: str, lastVni: str) -> bytes:
        """This method is used to create VNI pools

        Args:
            poolName (str): Name of the pool to be created
            firstVni (str): Frist VNI address 
            lastVni (str): Last VNI address

        Returns:
            bytes: Request response object
        """        
        url = self.baseUrl + self.urlVniPool

        data = f''' {{ "display_name": "{poolName}",
                        "ranges": [
                            {{
                            "first": "{firstVni}",
                            "last": "{lastVni}"
                            }}
                        ],
                        "id": "{poolName}"
                    }}'''

        response = self.urlRequest(url=url, method='POST', data=data)
        return response

    def resourceVniDelete(self, poolName: str) -> bytes:
        """Used to delete IP pools via the resourse ID

        Args:
            poolName (str): Name of the pool you wish to delete

        Returns:
            bytes: Request response object
        """        
        url = self.baseUrl + self.urlVniPool + '/' + poolName
        response = self.urlRequest(url=url, method='DELETE')
        return response

    def resourceVniGet(self) -> bytes:
        """Pulls information on all pools

        Returns:
            bytes: Request response 
        """        
        url = self.baseUrl + self.urlVniPool
        response = self.urlRequest(url=url, method='GET')
        return response
