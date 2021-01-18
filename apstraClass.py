"""
TODO:

    - Create configlet
    - Create the way you asign QFX to blueprint
    - Create VRF (Securuty Route)
    - Create VNIs Virtual Network
    - Assign Interface to server facing ports

    - Create Simple CLI
    - Create YAML Upload

"""
import requests
import time
import json

requests.packages.urllib3.disable_warnings() #Supress SSL verify warnings
response = requests.models.Response #python typing
 
class apstra():
    """Class init lists all the info globaly doe URI and Login
    """    
    def __init__(self):
        self.password = None
        self.username = None
        self.address = None
        self.port = None
        self.baseUrl = None
        self.apiToken = None

        #ResourcesURL
        self.urlAsnPool = '/api/resources/asn-pools'
        self.urlIpPool = '/api/resources/ip-pools'
        self.urlVniPool = '/api/resources/vni-pools'

        #Onboading
        self.systemAgent = '/api/system-agents'
        self.systems = '/api/systems/'
        self.systemsBatchUpdate = '/api/systems-batch-update/'

        #Design
        self.rackDesign = '/api/design/rack-types'
        self.templateDesign = '/api/design/templates'
        self.logicalDeviceDesign = '/api/design/logical-devices'

        #Blueprint
        self.blueprints = '/api/blueprints'
        self.blueprintsResouceGroupAsnSpine = '/resource_groups/asn/spine_asns'
        self.blueprintsResouceGroupAsnLeaf = '/resource_groups/asn/leaf_asns'
        self.blueprintsResouceGroup = '/resource_groups'
        self.blueprintsResouceGroupLoopbackSpine = '/resource_groups/ip/spine_loopback_ips'
        self.blueprintsResouceGroupLoopbackLeaf = '/resource_groups/ip/leaf_loopback_ips'
        self.blueprintsResouceGroupSpineLeafLink = '/resource_groups/ip/spine_leaf_link_ips'
        self.blueprintsResouceGroupVni = '/resource_groups/vni/evpn_l3_vnis'
        self.blueprintDeviceId = '/cabling-map'
        self.blueprintInterfaceMapAssignments='/interface-map-assignments'
        self.blueprintSecurityZone = '/security-zones'
        self.blueprintVirtualNetworks = '/virtual-networks-batch'

        #Demo Specific
        self.demoCustomerName = None
        self.demoTemplateName = None
        self.demoBlueprintName = None

    """
    Request Handling
    """
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
        print(f'\n\n{url}')

        try:
            if self.apiToken == None:
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache" }
                data = '{ \"username\":\"' + self.username + '\", \"password\":\"' + self.password + '\" }'
                response = requests.request(f"{method}", url, data=data, headers=headers, verify=False) 
                return response

            elif method == 'GET':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("GET", url, data=data, headers=headers, verify=False) 
            
            elif method == 'DELETE':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("DELETE", url, data=data, headers=headers, verify=False) 

            elif method == 'POST':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("POST", url, data=data, headers=headers, verify=False) 

            elif method == 'PUT':
                headers = { 'Content-Type':"application/json", 'Cache-Control':"no-cache", 'AUTHTOKEN':f"{self.apiToken}"}
                response = requests.request("PUT", url, data=data, headers=headers, verify=False) 

            print(f'{response.status_code} \n\n')

            return response
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


    """
    Login
    """
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
        self.getApiToken()

    def getApiToken(self):
        """Create new API token

        Creates new API token by loging in. The new token is saved as a instance
        varible.
        """        
        loginUrl = self.baseUrl + '/api/user/login'
        self.apiToken = None
        response = self.urlRequest(url=loginUrl, method='POST')
        self.apiToken = response.json()['token']
        print(self.apiToken)
        
    def createBaseUrl(self):
        """Create the base URL

        Creates the base URL using the address and port number. This is used by 
        every other instance
        """        
        self.baseUrl = 'https://' + self.address + ':' + self.port 


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
        returnedDic = response.json()
        returnedDic['totalPoolCount'] = len(returnedDic['items'])
        return returnedDic


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


    """
    Device Onboarding/Managing Devices
    """
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

        for dev in devList['items']:
            systemId = dev['id']
            deviceModel = dev['facts']['aos_hcl_model']
            self.ackManagedDevices(systemId, deviceModel)
            
    def systemsGet(self) -> bytes:
        """Get all system ID's

        Returns:
            bytes: Response Return
        """        
        url = self.baseUrl + self.systems
        response = self.urlRequest(url=url, method='GET')
        return response


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

    """
    Blueprints
    """
    #Resouce Group
    def blueprintCreate(self, blueprintName: str, templateName: str, designType: str = 'two_stage_l3clos') -> bytes:
        """Create a base blueprint

        Args:
            blueprintName (str): Name of blueprint
            templateName (str): Name of DC template to use with blueprint
            designType (str, optional): Type of blueprint design. Defaults to 'two_stage_l3clos'.

        Returns:
            bytes: Request response
        """        

        url = self.baseUrl + self.blueprints

        data = f'''
            {{"design":"{designType}", 
            "init_type":"template_reference",
            "label":"{blueprintName}",
            "template_id":"{templateName}", 
            "id":"{blueprintName}"}}
        '''
        response = self.urlRequest(url=url, method='POST', data=data)
        return response

    def blurprintResouceGroupAsnSpine(self, blueprintName: str, asnPool: str) -> bytes:
        """Asign ASN pool to blueprint - Spines

        Args:
            blueprintName (str): Name of blueprint 
            asnPool (str): ASN pool asigned to blueprint

        Returns:
            bytes: Request response
        """       
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroupAsnSpine
        data = f'''
                {{"pool_ids":["{asnPool}"]}}
            '''
        response = self.urlRequest(url=url, method='PUT', data=data)
        return response

    def blurprintResouceGroupAsnLeaf(self, blueprintName: str, asnPool: str) -> bytes:
        """Asign ASN pool to blueprint - Leafs

        Args:
            blueprintName (str): Name of blueprint 
            asnPool (str): ASN pool asigned to blueprint

        Returns:
            bytes: Request response
        """             
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroupAsnLeaf
        data = f'''
                {{"pool_ids":["{asnPool}"]}}
            '''
        response = self.urlRequest(url=url, method='PUT', data=data)
        return response 

    def blurprintResouceGroupIpSpine(self, blueprintName: str, ipPool: str) -> bytes:
        """Asign IP pool to blueprint - Spine

        Args:
            blueprintName (str): Name of blueprint 
            ipPool (str): IP pool asigned to blueprint

        Returns:
            bytes: Request response
        """   
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroupLoopbackSpine
        data = f'''
                {{"pool_ids":["{ipPool}"]}}
            '''
        response = self.urlRequest(url=url, method='PUT', data=data)
        return response 

    def blurprintResouceGroupIpLeaf(self, blueprintName: str, ipPool: str) -> bytes:
        """Asign IP pool to blueprint - Leafs

        Args:
            blueprintName (str): Name of blueprint 
            ipPool (str): IP pool asigned to blueprint

        Returns:
            bytes: Request response
        """   
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroupLoopbackLeaf
        data = f'''
                {{"pool_ids":["{ipPool}"]}}
            '''
        response = self.urlRequest(url=url, method='PUT', data=data)
        return response 

    def blurprintResouceGroupSpineLeafLink(self, blueprintName: str, ipPool: str) -> bytes:
        """Asign IP pool to blueprint - Inter-fabric Links

        Args:
            blueprintName (str): Name of blueprint 
            ipPool (str): IP pool asigned to blueprint

        Returns:
            bytes: Request response
        """   
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroupSpineLeafLink
        data = f'''
                {{"pool_ids":["{ipPool}"]}}
            '''
        response = self.urlRequest(url=url, method='PUT', data=data)
        return response 

    def blueprintDeviceIdGet(self, blueprintName: str) -> bytes:
        """Get the ID's of all devices in the blueprint

        Args:
            blueprintName (str): Name of blueprint 

        Returns:
            bytes: Request response
        """          
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintDeviceId
        idList=[]
        response = self.urlRequest(url=url, method='GET')
        for id in response.json()['links']:
            id=id['endpoints']
            for value in id:
                idList.append(value['system'])

        return idList

    def blueprintInterfaceMap(self, blueprintName: str, spinePhysicalDevcie: str, leafPhysicalDevice: str) -> bytes:
        """Asign the interface mapping of logical devices to physical device models

        Args:
            blueprintName (str): Name of blueprint 
            spinePhysicalDevcie (str): Spine physical device model i.e. Juniper_vQFX__AOS-7x10-Spine
            leafPhysicalDevice (str): Leaf physical device model i.e. Juniper_vQFX__AOS-7x10-Leaf

        Returns:
            bytes: Request response
        """   
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintInterfaceMapAssignments

        idList=self.blueprintDeviceIdGet(blueprintName=blueprintName)
        physicalDeviceMap={}
        for id in idList:
            if id['role'] == 'spine':
                physicalDeviceMap[id['id']] = spinePhysicalDevcie
            elif id['role'] == 'leaf':
                physicalDeviceMap[id['id']] = leafPhysicalDevice

        data=f'''
            {{"assignments":
                {json.dumps(physicalDeviceMap)}
            }}
            '''

        response = self.urlRequest(url=url, method='PUT', data=data)
        return response
    #Security Zones
    def blueprintCreateSecurityZone(self, securityZoneName: str, blueprintName: str) -> bytes:
        """Create a security zone within a blueprint

        Args:
            securityZoneName (str): Name of security zone
            blueprintName (str): Name of blueprint

        Returns:
            bytes: Request response
        """          
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintSecurityZone
        data = f'''

            {{
                "sz_type": "evpn",
                "label": "{securityZoneName}",
                "vrf_name": "{securityZoneName}"
            }}

        '''
        response = self.urlRequest(url=url, method='POST', data=data)
        return response.json()

    def blueprintGetSecurityZone(self, blueprintName: str) -> dict:
        """Get info on all security zones

        Args:
            blueprintName (str): Name of blueprint

        Returns:
            dict: Request response of security zone ID's
        """  
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintSecurityZone
        response = self.urlRequest(url=url, method='GET')
        return response.json()

    def blueprintAddSecurityZoneLoopbacks(self, securityZoneName: str, blueprintName: str, ipPool: str) -> dict:
        """Add loopback pool to security zone

        Args:
            blueprintName (str): Name of blueprint
            securityZoneName (str): Name of security zone
            ipPool (str): Name of pool

        Returns:
            dict: Request response of ID
        """  
        szId=None
        securityZones = self.blueprintGetSecurityZone(blueprintName)
        for key, value in securityZones['items'].items():
            if value['vrf_name'] == securityZoneName:
                szId=value['id']

        leafLoopback = 'sz%3A'+szId+'%2Cleaf_loopback_ips'

        data = f'''
            {{"pool_ids":["{ipPool}"]}}
        '''

        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroup + '/ip/' + leafLoopback

        response = self.urlRequest(url=url, method='PUT', data=data)
        return response.json()

    def blueprintAddSecurityZoneVNI(self, securityZoneName: str, blueprintName: str, vniPoolName: str) -> dict:
        """Add VNI pool to security zone

        Args:
            blueprintName (str): Name of blueprint
            securityZoneName (str): Name of security zone
            vniPoolName (str): Name of pool

        Returns:
            dict: Request response of ID
        """
        data = f'''
            {{"pool_ids":["{vniPoolName}"]}}
        '''

        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroupVni

        response = self.urlRequest(url=url, method='PUT', data=data)
        return response.json()

    #Virtual Networks
    def blueprintAddVirtualNetworks(self, blueprintName: str, virtualNetworkName: str, securityZoneName: str, ipv4Subnet: str = 'null', ipv4Gateway: str = 'null') -> dict:
        """Add virtual networks to security zone

        By default a L2 only overlay is added, IP address information can optionally
        be added so the L3 GW exists in the overlay

        Args:
            blueprintName (str): Name of blueprint
            virtualNetworkName (str): Name of virtual network
            securityZoneName (str): Name of security zone this virtual network is attached to
            ipv4Subnet (str, optional): IP subnet with mask. Defaults to 'null'.
            ipv4Gateway (str, optional): IP gateway. Defaults to 'null'.

        Returns:
            dict: Request Response ID
        """        
        response = self.blueprintDeviceIdGet(blueprintName)
        deviceList=[]
        for device in response:
            if device['role'] == 'leaf':
                deviceList.append('"system_id": "'+device['id']+'"')

        deviceListJson=','.join(set(deviceList))
        
        #Security Zone ID needed to add virtual networks
        szId=None
        securityZones = self.blueprintGetSecurityZone(blueprintName)
        for key, value in securityZones['items'].items():
            if value['vrf_name'] == securityZoneName:
                szId=value['id']
        
        #L2 or L3 Overlay
        if ipv4Subnet == 'null':
            ipv4Enabled='false'
        else:
            ipv4Enabled='true'
            ipv4Gateway = '"'+ipv4Gateway+'"'
            ipv4Subnet = '"'+ipv4Subnet+'"'

        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintVirtualNetworks
        data = f'''
                {{
                    "virtual_networks": [
                        {{
                            "vn_type": "vxlan",
                            "virtual_gateway_ipv4": {ipv4Gateway},
                            "bound_to": [
                                {{
                                    {deviceListJson}
                                }}
                            ],
                            "ipv4_subnet": {ipv4Subnet},
                            "label": "{virtualNetworkName}",
                            "ipv4_enabled": {ipv4Enabled},
                            "security_zone_id": "{szId}"
                        }}
                    ]
                }}

            '''
        response = self.urlRequest(url=url, method='POST', data=data)
        return response.json()

    def blueprintAddVxlanVniPool(self, blueprintName: str, vniPoolName: str) -> dict:
        """Add VNI pool to virtual network

        Args:
            blueprintName (str): Name of blueprint
            vniPoolName (str): VNI pool name

        Returns:
            dict: Request response ID
        """        
        data = f'''
            {{"pool_ids":["{vniPoolName}"]}}
        '''
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroup + '/vni/vxlan_vn_ids'
        response = self.urlRequest(url=url, method='PUT', data=data)
        return response.json()


    """
    Error Catch
    """
    def catchErrors(self, response: bytes) -> None:
        """May be used to print errors from JSON return

        Args:
            response (bytes): Response from a URI request
        """        
        if 'errors' in response.json():
            print(response.json())


    """
    Demo Provisioning
    """
    def jclProvision(self, customerName: str) -> None:
        """Create the entire JCL testbed in one easy python call.

        This method is used to create the entire JCL testbed in one easy python call.
        This is static and you get no choices however it should work for many demos.

        Args:
            customerName (str): Name of the customer
        """       
        #Remove ll white space in customer name
        self.demoCustomerName=customerName.replace(' ', '')
        self.demoTemplateName=self.demoCustomerName + '_DC_Template'
        self.demoBlueprintName = self.demoCustomerName + '_DC_Blueprint'
        self.demoSecurityZone = self.demoCustomerName + '_VRF'
        
        #Create ASN Pools
        self.resourceAsnCreate(poolName=self.demoCustomerName+'_ASN_Pool', firstAsn=65000, lastAsn=65500)
        
        #Little snooze
        time.sleep(1)
        
        #Create IP Pools
        ipPoolList=[{'name':'Fabric', 'subnet':'10.0.0.0/24'}, {'name':'Loopback', 'subnet':'172.16.0.0/24'}]
        for ipPool in ipPoolList:
            self.resourceIpCreate(poolName=self.demoCustomerName+'_'+ipPool['name']+'_IP_Pool', network=ipPool['subnet']) 

        #Little snooze
        time.sleep(1)

        #Create VNI Pools
        vniPoolList=[{'name':'default', 'firstVni':'6000', 'lastVni':'7000'}]
        for vniPool in vniPoolList:
            self.resourceVniCreate(poolName=self.demoCustomerName+'_'+vniPool['name']+'_VNI_Pool', \
                    firstVni=vniPool['firstVni'], lastVni=vniPool['lastVni'])

        #Little snooze
        time.sleep(1)

        #Create Rack Types
        rackTypeList=[
            {'rackName':'1Leaf1Server', 
            'connectivityType':'l2',
            'leafLogicalDevice':'AOS-7x10-Leaf',
            'serverCount':1,
            'serverLogicalDevice':'AOS-1x10-1',
            'leafServerLinkName':'ServerToLeaf'},
            
            {'rackName':'1Leaf2Server', 
            'connectivityType':'l2',
            'leafLogicalDevice':'AOS-7x10-Leaf',
            'serverCount':2,
            'serverLogicalDevice':'AOS-1x10-1',
            'leafServerLinkName':'ServerToLeaf'},
            ]
        for rackType in rackTypeList:
            self.createDesignSimpleRack(rackTypeName=rackType['rackName'], connectivityType=rackType['connectivityType'], \
                    leafLogicalDevice=rackType['leafLogicalDevice'], serverCount=rackType['serverCount'], \
                    serverLogicalDevice=rackType['serverLogicalDevice'], leafServerLinkName=rackType['leafServerLinkName'])

        #Little snooze
        time.sleep(1)

        #Create Template
        self.designDemoTemplate(templateName=self.demoTemplateName, spineLogicalDeviceId='AOS-7x10-Spine', \
                rackTypeList=['1Leaf1Server', '1Leaf2Server'], spineCount=2, ipChoice='ipv4', asnAllocation='distinct', \
                overlayControl='evpn')

        #Little snooze
        time.sleep(1)

        #Create Blueprint
        self.blueprintCreate(blueprintName=self.demoBlueprintName, templateName=self.demoTemplateName)

        time.sleep(5)

        #Asign ASN and IP pools
        self.blurprintResouceGroupAsnSpine(blueprintName=self.demoBlueprintName, asnPool=self.demoCustomerName+'_ASN_Pool')
        self.blurprintResouceGroupAsnLeaf(blueprintName=self.demoBlueprintName, asnPool=self.demoCustomerName+'_ASN_Pool')
        self.blurprintResouceGroupIpSpine(blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Loopback_IP_Pool')
        self.blurprintResouceGroupIpLeaf(blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Loopback_IP_Pool')
        self.blurprintResouceGroupSpineLeafLink(blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Fabric_IP_Pool')

        #Little snooze
        time.sleep(1)

        #Asign Physical devcie templates to logical devices
        self.blueprintInterfaceMap(blueprintName=self.demoBlueprintName, spinePhysicalDevcie='Juniper_vQFX__AOS-7x10-Spine', leafPhysicalDevice='Juniper_vQFX__AOS-7x10-Leaf')

        #Little snooze
        time.sleep(1)

        #Create security zone (VRF)
        self.blueprintCreateSecurityZone(securityZoneName=self.demoSecurityZone, blueprintName=self.demoBlueprintName)

        #Little snooze
        time.sleep(10)

        #Add Loopback addresses for the new VRF
        self.blueprintAddSecurityZoneLoopbacks(securityZoneName=self.demoSecurityZone, blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Loopback_IP_Pool')

        #Little snooze
        time.sleep(1)

        #Add VNI to the security zone
        self.blueprintAddSecurityZoneVNI(securityZoneName=self.demoSecurityZone, blueprintName=self.demoBlueprintName, vniPoolName=self.demoCustomerName+'_default_VNI_Pool')

        #Little snooze
        time.sleep(1)

        #Add VXLAN VNI's
        vxlanList=[{'name':f'{self.demoCustomerName}_VNI_RED', 'ipv4Subnet':'192.168.1.0/24', 'ipv4Gateway':'192.168.1.1'}, {'name':f'{self.demoCustomerName}_VNI_BLUE', 'ipv4Subnet':'192.168.2.0/24', 'ipv4Gateway':'192.168.2.1'}]
        for vxlan in vxlanList:
            self.blueprintAddVirtualNetworks(blueprintName=self.demoBlueprintName, virtualNetworkName=vxlan['name'], securityZoneName=self.demoSecurityZone, \
                ipv4Subnet=vxlan['ipv4Subnet'], ipv4Gateway=vxlan['ipv4Gateway'])

        #Little snooze
        time.sleep(1)

        #Assign VNI pool to the virtual VXLAN networks
        self.blueprintAddVxlanVniPool(blueprintName=self.demoBlueprintName, vniPoolName=self.demoCustomerName+'_default_VNI_Pool')

        #Little snooze
        time.sleep(1)

        #Onboard Devices
        self.offboxOnboarding(username='root', password='Juniper!1', platform='junos', \
                mgmtIpList=['100.123.13.201', '100.123.13.202', '100.123.13.203', '100.123.13.204'])

        #Quick snooze while the offbox agent is set up
        time.sleep(20)

        #Ack All Devices
        self.ackManagedDevicesAll()

