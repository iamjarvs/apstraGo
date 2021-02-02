"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================

"""
import requests
import json
    
class blueprints():

    def __init__(self):
        super().__init__() 

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

    def blueprintInfoGet(self, blueprintName: str ='') -> bytes:
        """Blueprint Physical Devcie Assignment

        Args:
            blueprintName (str, optional)): Name of blueprint

        Returns:
            bytes: Request response
        """        
        url = self.baseUrl + self.blueprints + '/' + blueprintName

        response = self.urlRequest(url=url, method='GET')
        return response

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
    
    def blueprintPhysicalDevcieAssignment(self, blueprintName: str, blueprintDeviceId: str, deviceSN: str):
        """Blueprint Physical Devcie Assignment

        Args:
            blueprintName (str): Name of blueprint
            templateName (str): Name of DC template to use with blueprint
            designType (str, optional): Type of blueprint design. Defaults to 'two_stage_l3clos'.

        Returns:
            bytes: Request response
        """  
        url = self.baseUrl + self.blueprints + '/' + blueprintName + '/nodes/' + blueprintDeviceId
        data = f'''
            {{"system_id":"{deviceSN}", "deploy_mode":"deploy"}}
        '''

        response = self.urlRequest(url=url, method='PATCH', data=data)
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
        return response

    def blueprintGetSecurityZone(self, blueprintName: str) -> dict:
        """Get info on all security zones

        Args:
            blueprintName (str): Name of blueprint

        Returns:
            dict: Request response of security zone ID's
        """  
        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintSecurityZone
        response = self.urlRequest(url=url, method='GET')
        return response

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
        responses = self.blueprintGetSecurityZone(blueprintName)
        securityZones = responses.json()
        for key, value in securityZones['items'].items():
            if value['vrf_name'] == securityZoneName:
                szId=value['id']

        leafLoopback = 'sz%3A'+szId+'%2Cleaf_loopback_ips'

        data = f'''
            {{"pool_ids":["{ipPool}"]}}
        '''

        url = self.baseUrl + self.blueprints + '/' + blueprintName + self.blueprintsResouceGroup + '/ip/' + leafLoopback

        response = self.urlRequest(url=url, method='PUT', data=data)
        return response

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
        return response

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
                deviceList.append('{"system_id": "'+device['id']+'"}')

        deviceListJson=','.join(set(deviceList))
        
        #Security Zone ID needed to add virtual networks
        szId=None
        responses = self.blueprintGetSecurityZone(blueprintName)
        securityZones = responses.json()
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
                                    {deviceListJson}
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
        return response

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
        return response