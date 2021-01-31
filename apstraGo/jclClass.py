"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================
"""
import json
try:
    import apstraClass
except ModuleNotFoundError as e:
    pass
try:
    from apstraGo import apstraClass
except ModuleNotFoundError as e:
    pass
import time
import requests

class jcl(apstraClass.apstra):
    """JCL/vLabs Auto-creation class

    This class aims to provide a set blueprint for creating a AOS demo testbed.
    The following happens:
        - Creates all resource pools
        - Creates rack types
        - Creates DC template
        - Creates blueprint
        - Asigns resource pools to blueprint
        - Creates security zone in blueprint
        - Creates virtual networks in blueprint
        - Onboards vLabs/JCL deivces

    Once this has run you just need just need to assign the devices to the blueprint
    and assign ports to the virtual network.

    """    
    def __init__(self):
        super().__init__()
        self.demoCustomerName=None
        self.demoTemplateName=None
        self.demoBlueprintName=None
        self.demoSecurityZone=None

    def demoAsnPool(self, poolName, firstAsn, lastAsn):
        #Create ASN Pools
        response=self.resourceAsnCreate(poolName=poolName, firstAsn=firstAsn, lastAsn=lastAsn)
        self.responseParse(response)

    def demoIpPool(self, poolName, network):
        #Create IP Pools
        response=self.resourceIpCreate(poolName=poolName, network=network)
        self.responseParse(response)

    def createVniPool(self, poolName, firstVni, lastVni):
        #Create VNI Pools
        response=self.resourceVniCreate(poolName=poolName, firstVni=firstVni, lastVni=lastVni)
        self.responseParse(response)

    def createRacks(self):
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
            response=self.createDesignSimpleRack(rackTypeName=rackType['rackName'], connectivityType=rackType['connectivityType'], \
                    leafLogicalDevice=rackType['leafLogicalDevice'], serverCount=rackType['serverCount'], \
                    serverLogicalDevice=rackType['serverLogicalDevice'], leafServerLinkName=rackType['leafServerLinkName'])
            self.responseParse(response)

    def createDcTemplate(self):
        #Create Template
        response=self.designDemoTemplate(templateName=self.demoTemplateName, spineLogicalDeviceId='AOS-7x10-Spine', \
                rackTypeList=['1Leaf1Server', '1Leaf2Server'], spineCount=2, ipChoice='ipv4', asnAllocation='distinct', \
                overlayControl='evpn')
        self.responseParse(response)

    def createBlueprint(self):
        #Create Blueprint
        response=self.blueprintCreate(blueprintName=self.demoBlueprintName, templateName=self.demoTemplateName)
        self.responseParse(response)

    def blueprintPools(self): 
        #Asign ASN and IP pools
        response=self.blurprintResouceGroupAsnSpine(blueprintName=self.demoBlueprintName, asnPool=self.demoCustomerName+'_ASN_Pool')
        self.responseParse(response)
        response=self.blurprintResouceGroupAsnLeaf(blueprintName=self.demoBlueprintName, asnPool=self.demoCustomerName+'_ASN_Pool')
        self.responseParse(response)
        response=self.blurprintResouceGroupIpSpine(blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Loopback_IP_Pool')
        self.responseParse(response)
        response=self.blurprintResouceGroupIpLeaf(blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Loopback_IP_Pool')
        self.responseParse(response)
        response=self.blurprintResouceGroupSpineLeafLink(blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Fabric_IP_Pool')
        self.responseParse(response)

    def blueprintInterfaceMapping(self):
        #Asign Physical devcie templates to logical devices
        response=self.blueprintInterfaceMap(blueprintName=self.demoBlueprintName, spinePhysicalDevcie='Juniper_vQFX__AOS-7x10-Spine', leafPhysicalDevice='Juniper_vQFX__AOS-7x10-Leaf')

    def blueprintVrf(self):
        #Create security zone (VRF)
        response=self.blueprintCreateSecurityZone(securityZoneName=self.demoSecurityZone, blueprintName=self.demoBlueprintName)
        self.responseParse(response)

    def blueprintVrfLoopbacks(self):
        #Add Loopback addresses for the new VRF
        response=self.blueprintAddSecurityZoneLoopbacks(securityZoneName=self.demoSecurityZone, blueprintName=self.demoBlueprintName, ipPool=self.demoCustomerName+'_Loopback_IP_Pool')
        self.responseParse(response)

    def blueprintPhysicalAssignment(self):

        responseBlueprint=self.blueprintInfoGet(blueprintName=self.demoBlueprintName)
        responseDevices=self.systemsGet()

        for key, value in responseBlueprint.json()['nodes'].items():
            device = value.get('role')
            if device != None:
                if 'spine1' in value['label'] and value.get('system_type') == 'switch':
                    for sysDevice in responseDevices.json()['items']:
                        if sysDevice['facts']['mgmt_ipaddr'] == '100.123.13.201':
                            response=self.blueprintPhysicalDevcieAssignment(blueprintName=self.demoBlueprintName, \
                                        blueprintDeviceId=value['id'], deviceSN=sysDevice['device_key'])
                            self.responseParse(response)
                elif 'spine2' in value['label'] and value.get('system_type') == 'switch':
                    for sysDevice in responseDevices.json()['items']:
                        if sysDevice['facts']['mgmt_ipaddr'] == '100.123.13.202':
                            response=self.blueprintPhysicalDevcieAssignment(blueprintName=self.demoBlueprintName, \
                                        blueprintDeviceId=value['id'], deviceSN=sysDevice['device_key'])
                            self.responseParse(response)
                elif '1leaf1server' in value['label'] and value.get('system_type') == 'switch':
                    for sysDevice in responseDevices.json()['items']:
                        if sysDevice['facts']['mgmt_ipaddr'] == '100.123.13.203':
                            response=self.blueprintPhysicalDevcieAssignment(blueprintName=self.demoBlueprintName, \
                                        blueprintDeviceId=value['id'], deviceSN=sysDevice['device_key'])
                            self.responseParse(response)
                elif '1leaf2server' in value['label'] and value.get('system_type') == 'switch':
                    for sysDevice in responseDevices.json()['items']:
                        if sysDevice['facts']['mgmt_ipaddr'] == '100.123.13.204':
                            response=self.blueprintPhysicalDevcieAssignment(blueprintName=self.demoBlueprintName, \
                                        blueprintDeviceId=value['id'], deviceSN=sysDevice['device_key'])
                            self.responseParse(response)

    def blueprintVrfVni(self):
        #Add VNI to the security zone
        response=self.blueprintAddSecurityZoneVNI(securityZoneName=self.demoSecurityZone, blueprintName=self.demoBlueprintName, vniPoolName=self.demoCustomerName+'_default_VNI_Pool')
        self.responseParse(response)

    def virtualNetworkVxlans(self):
        #Add VXLAN VNI's
        vxlanList=[{'name':f'{self.demoCustomerName}_VN1', 'ipv4Subnet':'192.168.100.0/24', 'ipv4Gateway':'192.168.100.1'}, {'name':f'{self.demoCustomerName}_VN2', 'ipv4Subnet':'192.168.200.0/24', 'ipv4Gateway':'192.168.200.1'}]
        for vxlan in vxlanList:
            response=self.blueprintAddVirtualNetworks(blueprintName=self.demoBlueprintName, virtualNetworkName=vxlan['name'], securityZoneName=self.demoSecurityZone, \
                ipv4Subnet=vxlan['ipv4Subnet'], ipv4Gateway=vxlan['ipv4Gateway'])
            self.responseParse(response)

    def virtualNetworkVni(self):
        #Assign VNI pool to the virtual VXLAN networks
        response=self.blueprintAddVxlanVniPool(blueprintName=self.demoBlueprintName, vniPoolName=self.demoCustomerName+'_default_VNI_Pool')
        self.responseParse(response)
        
    def onboardDevices(self):
        #Onboard Devices
        responseAll=self.offboxOnboarding(username='root', password='Juniper!1', platform='junos', \
                mgmtIpList=['100.123.13.201', '100.123.13.202', '100.123.13.203', '100.123.13.204'])
        for response in responseAll:
            self.responseParse(response)

    def ackAllDevices(self):
        #Ack All Devices
        self.ackManagedDevicesAll()
        self.customSuccess(response="\n     All Devices Acknowledged\n")

    def responseParse(self, response):
        try:
            if 'errors' in response.json():
                self.customError(response)
            else:
                self.customSuccess(response)
        except json.JSONDecodeError as e:
            self.customError(response=e)

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
        self.demoAsnPool(poolName=self.demoCustomerName+'_ASN_Pool', firstAsn=65000, lastAsn=65500)
        #Little snooze
        time.sleep(1)
        # Create IP Pools
        ipPoolList=[{'name':'Fabric', 'subnet':'10.0.0.0/24'}, {'name':'Loopback', 'subnet':'172.16.0.0/24'}]
        for ipPool in ipPoolList:
            self.demoIpPool(poolName=self.demoCustomerName+'_'+ipPool['name']+'_IP_Pool', network=ipPool['subnet'])
        #Little snooze
        time.sleep(1)
        #Create VNI Pools
        vniPoolList=[{'name':'default', 'firstVni':'6000', 'lastVni':'7000'}]
        for vniPool in vniPoolList:
            self.createVniPool(poolName=self.demoCustomerName+'_'+vniPool['name']+'_VNI_Pool', \
                    firstVni=vniPool['firstVni'], lastVni=vniPool['lastVni'])
        #Little snooze
        time.sleep(1)
        #Create Rack Types
        self.createRacks()
        #Little snooze
        time.sleep(1)
        #Create Template
        self.createDcTemplate()
        #Little snooze
        time.sleep(1)
        #Create Blueprint
        self.createBlueprint()
        #Little snooze
        time.sleep(5)
        #Asign ASN and IP pools
        self.blueprintPools()
        #Little snooze
        time.sleep(1)
        #Asign Physical devcie templates to logical devices
        self.blueprintInterfaceMapping()
        #Little snooze
        time.sleep(1)
        #Create security zone (VRF)
        self.blueprintVrf()
        #Little snooze
        time.sleep(1)
        #Add Loopback addresses for the new VRF
        self.blueprintVrfLoopbacks()
        #Little snooze
        time.sleep(1)
        #Add VNI to the security zone
        self.blueprintVrfVni()
        #Little snooze
        time.sleep(1)
        #Add VXLANs
        self.virtualNetworkVxlans()
        #Little snooze
        time.sleep(1)
        #Add VXLAN VNI's
        self.virtualNetworkVni()
        #Onboard Devices
        self.onboardDevices()
        #Quick snooze while the offbox agent is set up
        time.sleep(20)
        #Ack All Devices
        self.ackAllDevices()
        #Quick snooze 
        time.sleep(5)
        #Assign physical devices to blueprint
        self.blueprintPhysicalAssignment()

if __name__ == "__main__":
    pass