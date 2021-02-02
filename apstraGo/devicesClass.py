"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
import requests
import json
    
class devices():

    def __init__(self):
        super().__init__()

    def offboxOnboarding(self, username: str, password: str, platform: str, mgmtIpList: list, \
            resId:str ='', agent_type: str ='offbox', operation_mode: str ='full_control') -> None:
        """This method is used to onboard off box agent devices

        Args:
            username (str): Network device username
            password (str): Network devcie password
            platform (str): Network device platform
            mgmtIpList (list): Network devcie IP
            agent_type (str): Apstra agent type i.e. onbox or offbox (only offbox supported atm). Defaults to offbox
            operation_mode (str): Apstra control i.e. full_control. Defaults to full_control
            resId (str, optional): Resouce ID. Defaults to ''.
        """
        url = self.baseUrl + self.systemAgent

        if resId == '':
            idString = ''
        elif resId != '':
            idString = f'"id": "{resId}",'

        responseAll = []
        for mgmtIp in mgmtIpList:

            data = f'''{{
                            "username": "{username}",
                            "password": "{password}",
                            "job_on_create": "check",
                            "platform": "{platform}",
                            "management_ip": "{mgmtIp}",
                            {idString}
                            "agent_type": "{agent_type}",
                            "operation_mode": "{operation_mode}"
                        }}'''

            response = self.urlRequest(url=url, method='POST', data=data)
            responseAll.append(response)

        return responseAll
        
    def ackManagedDevices(self, systemId: str, deviceModel: str) -> bytes:
        """Acknowledge devices added to Apstra

        Args:
            systemId (str): The ID of the device in AOS
            deviceModel (str): The device type

        Returns:
            bytes: Request response
        """        

        url = self.baseUrl + self.systemsBatchUpdate

        data = f'''{{"{systemId}": 
                        {{"user_config": 
                            {{
                                "aos_hcl_model": "{deviceModel}", 
                                "admin_state": "normal"
                            }}
                        }}
                    }}'''
        response = self.urlRequest(url=url, method='POST', data=data)
        return response

    def ackManagedDevicesAll(self) -> bytes:
        """Acknowledges every device in AOS

        Returns:
            bytes: Response return
        """        
        devList = self.systemsGet().json()

        responseAll = []
        for dev in devList['items']:
            systemId = dev['id']
            deviceModel = dev['facts']['aos_hcl_model']
            response = self.ackManagedDevices(systemId, deviceModel)
            responseAll.append(response)

        return responseAll
           
    def systemsGet(self) -> bytes:
        """Get all system ID's

        Returns:
            bytes: Response Return
        """        
        url = self.baseUrl + self.systems
        response = self.urlRequest(url=url, method='GET')
        return response