"""
==========================================
 Title:  ApstraGo
 Author: Adam Jarvis
 Date:   2021
==========================================
TODO:
    - Create configlet

"""

try:
    import urlHandlingClass
    import loginClass
    import resourcePoolsClass
    import devicesClass
    import designClass
    import blueprintsClass
    import erorrHandlingClass
except ModuleNotFoundError as e:
    pass
try:
    from apstraGo import urlHandlingClass
    from apstraGo import loginClass
    from apstraGo import resourcePoolsClass
    from apstraGo import devicesClass
    from apstraGo import designClass
    from apstraGo import blueprintsClass
    from apstraGo import erorrHandlingClass
except ModuleNotFoundError as e:
    pass

    
import requests
import json
 
class apstra(urlHandlingClass.urlRequests, loginClass.login, resourcePoolsClass.resourcePools, devicesClass.devices, \
                designClass.design, blueprintsClass.blueprints, erorrHandlingClass.errors):
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

