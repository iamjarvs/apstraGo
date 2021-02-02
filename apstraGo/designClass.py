"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
import requests
import json
    
class design():

    def __init__(self):
        super().__init__() 
    
    """
    Design.LogicalDevices
    """
    def getDesignLogicalDesign(self, devId='') -> bytes:
        """Pulls information on all or one logical device type

        Args:
            devId (str, optional): Logical device ID. Defaults to ''.

        Returns:
            bytes: Request Response
        """        
        url = self.baseUrl + self.logicalDeviceDesign + '/' + devId
        response = self.urlRequest(url=url, method='GET')
        return response


    """
    Design.Racks
    """
    def createDesignSimpleRack(self, rackTypeName: str, **kwargs: dict) -> bytes:
        """This method is just for simple rack designs - 1 leafs, no redundency, no lag ---> Simples

        Args:
            rackTypeName (str): Name of the rack that's being created.

        Returns:
            bytes: Request Response
        """
        rackTypeDesc = kwargs.get('rackTypeDesc') or ''
        connectivityType = kwargs.get('connectivityType') or 'l2'

        leafName: str = kwargs.get('leafName') or rackTypeName + '-Leaf'
        leafLogicalDevice: str = kwargs.get('leafLogicalDevice') or 'AOS-7x10-Leaf'
        linksPerSpine: int = kwargs.get('linksPerSpine') or 1
        leafSpineLinkSpeedUnit: str = kwargs.get('leafSpineLinkSpeedUnit') or 'G'
        leafSpineLinkSpeedValue: int = kwargs.get('leafSpineLinkSpeedValue') or 10 

        serverName: str = kwargs.get('serverName') or rackTypeName + '-Server'
        serverCount: int = kwargs.get('serverCount') or 1
        serverLogicalDevice: str = kwargs.get('serverLogicalDevice') or 'AOS-1x10-1'
        leafServerLinkName: str = kwargs.get('leafServerLinkName') or 'ServerToLeaf'
        lagType: str = kwargs.get('lagType') or 'null'
        LeafServerLinkSpeedUnit: str = kwargs.get('LeafServerLinkSpeedUnit') or 'G'
        LeafServerLinkSpeedValue: int = kwargs.get('LeafServerLinkSpeedValue') or 10
        linksPerLeafCount: int = kwargs.get('linksPerLeafCount') or 1

        data = f'''{{
                    "display_name": "{rackTypeName}",
                    "id": "{rackTypeName}",
                    "description": "{rackTypeDesc}",
                    "servers": [
                        {{
                            "count": {serverCount},
                            "connectivity_type": "{connectivityType}",
                            "links": [
                                {{
                                    "link_per_switch_count": {linksPerLeafCount},
                                    "label": "{leafServerLinkName}",
                                    "link_speed": {{
                                        "unit": "{LeafServerLinkSpeedUnit}",
                                        "value": {LeafServerLinkSpeedValue}
                                    }},
                                    "target_switch_label": "{leafName}",
                                    "attachment_type": "singleAttached",
                                    "lag_mode": {lagType}
                                    }}
                                ],
                                "label": "{serverName}",
                                "ip_version": "ipv4",
                                "logical_device": "{serverLogicalDevice}"
                                }}
                            ],
                    "leafs": [
                        {{
                            "link_per_spine_count": {linksPerSpine},
                            "redundancy_protocol": null,
                            "link_per_spine_speed": {{
                                "unit": "{leafSpineLinkSpeedUnit}",
                                "value": {leafSpineLinkSpeedValue}
                            }},
                            "label": "{leafName}",
                            "logical_device": "{leafLogicalDevice}"
                        }}
                    ]
                }}'''

        url = self.baseUrl + self.rackDesign
        response = self.urlRequest(url=url, method='POST', data=data)
        return response

    def getDesignSimpleRack(self) -> bytes:
        """Get all rack designs

        Returns:
            bytes: Request Response
        """        
        url = self.baseUrl + self.rackDesign
        response = self.urlRequest(url=url, method='GET')
        return response


    """
    Design.Templates
    """
    def designDemoTemplate(self, templateName: str, spineLogicalDeviceId: str, rackTypeList: list=[], **kwargs: dict) -> bytes:
        """This  method is used to create a template 

        Args:
            templateName (str): Name of the template
            spineLogicalDeviceId (str): Logical device type you wish to use as spines, for example AOS-7x10-Spine
            rackTypeList (list, optional): List of racks you wish to have, duplicates needed if you multiple of the same. Defaults to [].

        Kwargs:
            spineCount (int): Number of spines you want for this template
            ipChoice (int): Fabric IP type (ipv4/ipv6)
            asnAllocation (str): How the underlay ASN's are configured (single/distinct)
            overlayControl (str) Overlay type (evpn/null)

        Returns:
            bytes: Response Request
        """        
        spineCount: str = kwargs.get('spineCount') or 2
        ipChoice: str = kwargs.get('ipChoice') or 'ipv4'
        asnAllocation: str = kwargs.get('asnAllocation') or 'distinct'
        overlayControl: str = kwargs.get('overlayControl') or 'evpn'

        rackJsonList = []

        #Rack Count
        rackCount = []
        rackCountDict = {i:rackTypeList.count(i) for i in rackTypeList}
        uniqueList = set(rackTypeList)
        for rackType in uniqueList:
            count = rackCountDict[rackType]
            rackCount.append(f'{{"rack_type_id": "{rackType}", "count": {count}}}')
    
        rackCountData = ','.join(rackCount)

        #Rack data for JSON Payload
        response = self.getDesignSimpleRack()
        for rackType in set(rackTypeList):
            for returnedRackType in response.json()['items']:
                if returnedRackType['display_name'] == rackType:
                    rackJsonList.append(json.dumps(returnedRackType))

        rackJsonList = ','.join(rackJsonList)
        
        #Spine data for JSON Payload
        spineLogicalDevice = self.getDesignLogicalDesign(spineLogicalDeviceId)
       
        data = f'''
                {{
                    "display_name":"{templateName}",
                    "external_routing_policy":{{
                    "import_policy":"default_only",
                    "export_policy":{{
                        "all_routes":true,
                        "loopbacks":true,
                        "spine_leaf_links":true,
                        "l2edge_subnets":true,
                        "l3edge_server_links":true
                        }}
                    }},
                    "rack_type_counts":[
                        {rackCountData}
                    ],
                    "asn_allocation_policy":{{
                        "spine_asn_scheme":"{asnAllocation}"
                    }},
                    "virtual_network_policy":{{
                        "overlay_control_protocol":"{overlayControl}"
                    }},
                    "type":"rack_based",
                    "fabric_addressing_policy":{{
                        "spine_leaf_links":"{ipChoice}"
                    }},
                    "dhcp_service_intent":{{
                        "active":true
                    }},
                    "spine":{{
                        "count":{spineCount},
                        "external_link_count":0,
                        "link_per_superspine_count":0,
                        "link_per_superspine_speed":null,
                        "external_link_speed":null,
                        "logical_device":
                            {json.dumps(spineLogicalDevice.json())}
                            
                    }},
                    "rack_types": [
                        {rackJsonList}
                    ],
                    "id":"{templateName}"

                }}           
        '''

        url = self.baseUrl + self.templateDesign
        response = self.urlRequest(url=url, method='POST', data=data)
        return response