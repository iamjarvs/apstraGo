"""
This tool allows someone to define Apstra state and spine it up

Useful for demos

"""
from cerberus import Validator
from rich import print
try:
    from jclClass import jcl
except ModuleNotFoundError as e:
    pass
try:
    from apstraGo.jclClass import jcl
except ModuleNotFoundError as e:
    pass
import argparse
import yaml
import requests
import time
import os
import json

def yamlValidateFilePath() -> str:
    """Sets up path to data file in package

    Returns:
        str: path to data file
    """    
    this_dir, this_filename = os.path.split(__file__)
    return os.path.join(this_dir, "data", "yamlData.py")

def loadYaml(filepath: str) -> dict:
    """Load YAML File

    Args:
        filepath (str): Path to YAML config file

    Returns:
        dict: Reuturns YAML file as Dict
    """    
    with open(filepath, 'r') as stream:
        try:
            inputDict=yaml.safe_load(stream)
        except yaml.YAMLError as e:
            self.customError(errorInfo=e)
            exit(1)
    return inputDict

def yamlValidate(inputDict: dict, yamlValidateFilename: str) -> None:
    """Validates the user input YAML with template

    Args:
        inputDict (dict): User YAML Dict input
        yamlValidateFilename (str): YAML allowed values template
    """    
    
    #Open YAML validation file
    try:
        schema = eval(open(yamlValidateFilename, 'r').read())
    except (ValueError, SyntaxError) as e:
        self.customError(response=e)
        exit(1)
    
    #Compared input with allowed values
    try:
        v = Validator(schema)
        v.validate(inputDict, schema)
    except Exception as e:
        self.customError(response=e)
        exit(1)

    #Print and exit on error
    if bool(v.errors) is not False:
        self.customError(response=v.errors)
        exit(1)

def login(inputDict: dict) -> bytes:
    """Checks login details exist and creates instance of Apstra Class

    Args:
        inputDict (dict): YAML file Dict

    Returns:
        btyes: Returns Apstra instance object
    """    
    
    if "login" not in inputDict['apstrago']:
        self.customError(response="\nLogin Section Missing From YAML File\n")
        exit(1)    
    if "username" not in inputDict['apstrago']['login']:
        self.customError(response="\nUsername Missing From Login Section In YAML File\n")
        exit(1)
    if "password" not in inputDict['apstrago']['login']:
        self.customError(response="\nPassword Missing From Login Section In YAML File\n")
        print('error')
        exit(1)
    if "address" not in inputDict['apstrago']['login']:
        self.customError(response="\nAddress Missing From Login Section In YAML File\n")
        exit(1)

    con = jcl()
    response = con.login(username=inputDict['apstrago']['login']['username'], \
                password=inputDict['apstrago']['login']['password'], \
                address=inputDict['apstrago']['login']['address'], \
                port=inputDict['apstrago']['login'].get('port') or None, \
                customerName=inputDict['apstrago'].get('customerName'))

    if 'errors' in response.json():
        self.customError(response)
        exit(1)
    else:
        self.customSuccess(response)
        return con

def inputProcess(inputDict: dict, con: bytes) -> None:
    """Checks YAML doc sections

    Args:
        inputDict (dict): User YAML input
        con (bytes): JCL class instance object
    """    
    
    if 'resourcePools' in inputDict['apstrago']:
        resourcePools(inputs=inputDict['apstrago']['resourcePools'], con=con)

    if 'racks' in inputDict['apstrago']:
        rackCreation(inputs=inputDict['apstrago']['racks'], con=con)
    
    if 'templates' in inputDict['apstrago']:
        templateCreation(inputs=inputDict['apstrago']['templates'], con=con)

    if 'blueprints' in inputDict['apstrago']:
        blueprintCreation(inputs=inputDict['apstrago']['blueprints'], con=con)

    if 'devices' in inputDict['apstrago']:
        addDevices(inputs=inputDict['apstrago']['devices'], con=con)

def resourcePools(inputs: dict, con: bytes) -> None:
    """Creates Resource Pools if correct config present

    Args:
        inputDict (dict): User YAML input
        con (bytes): JCL class instance object
    """    
    if 'asnPools' in inputs:
        for item in inputs['asnPools']:
            response = con.resourceAsnCreate(poolName=item['poolName'], firstAsn=item['firstASN'], \
                    lastAsn=item['lastASN'])

            if 'errors' in response.json():
                self.customError(response)
            else:
                self.customSuccess(response)

    if 'ipPools' in inputs:
        for item in inputs['ipPools']:
            response = con.resourceIpCreate(poolName=item['poolName'], network=item['network'])

            if 'errors' in response.json():
                self.customError(response)
            else:
                self.customSuccess(response)

    if 'vniPools' in inputs:
        for item in inputs['vniPools']:
            response = con.resourceVniCreate(poolName=item['poolName'], firstVni=item['firstVNI'], lastVni=item['lastVNI'])

            if 'errors' in response.json():
                self.customError(response)
            else:
                self.customSuccess(response)

def rackCreation(inputs: dict, con:bytes) -> None:
    """Creates racks if config present

    Args:
        inputDict (dict): User YAML input
        con (bytes): JCL class instance object
    """    
    for item in inputs:
        response = con.createDesignSimpleRack(rackTypeName=item['rackName'], rackTypeDesc=item.get('rackTypeDesc') or None, \
                        connectivityType=item.get('connectivityType') or None, leafName=item.get('leafName') or None, \
                        leafLogicalDevice=item.get('leafLogicalDevice') or None, linksPerSpine=item.get('linksPerSpine') or None, \
                        leafSpineLinkSpeedUnit=item.get('leafSpineLinkSpeedUnit') or None, leafSpineLinkSpeedValue=item.get('leafSpineLinkSpeedValue') or None, \
                        serverName=item.get('serverName') or None, serverCount=item.get('serverCount') or None, \
                        serverLogicalDevice=item.get('serverLogicalDevice') or None, leafServerLinkName=item.get('leafServerLinkName') or None, \
                        lagType=item.get('lagType') or None, LeafServerLinkSpeedUnit=item.get('LeafServerLinkSpeedUnit') or None, \
                        LeafServerLinkSpeedValue=item.get('LeafServerLinkSpeedValue') or None, linksPerLeafCount=item.get('linksPerLeafCount') or None)

        if 'errors' in response.json():
            self.customError(response)
        else:
            self.customSuccess(response)

def templateCreation(inputs: dict, con: bytes) -> None:
    """Creates  DC templates if correct config present

    Args:
        inputDict (dict): User YAML input
        con (bytes): JCL class instance object
    """    
    for item in inputs:
        response = con.designDemoTemplate(templateName=item['templateName'], spineLogicalDeviceId=item['spineLogicalDeviceId'], \
                        rackTypeList=item['rackTypeList'], spineCount=item.get('spineCount') or None, ipChoice=item.get('ipChoice') or None, \
                        asnAllocation=item.get('asnAllocation') or None, overlayControl=item.get('overlayControl') or None)
        
        if 'errors' in response.json():
            self.customError(response)
        else:
            self.customSuccess(response)

def blueprintCreation(inputs: dict, con: bytes) -> None:
    """Creates blueprints if correct config present

    Args:
        inputDict (dict): User YAML input
        con (bytes): JCL class instance object
    """    
    for item in inputs:
        response = con.blueprintCreate(blueprintName=item['name'], templateName=item['templateName'])

        if 'errors' in response.json():
            self.customError(response)
        else:
            self.customSuccess(response)

def addDevices(inputs: dict, con: bytes) -> None:
    """Creates devices if correct config present

    Args:
        inputDict (dict): User YAML input
        con (bytes): JCL class instance object
    """    
    responseAll = con.offboxOnboarding(username=inputs['username'], password=inputs['password'], platform=inputs['platform'], \
                agent_type=inputs.get('agentType') or 'offbox', operation_mode=inputs.get('operationMode') or 'full_control', \
                mgmtIpList=inputs['addresses'])

    for response in responseAll:
        if 'errors' in response.json():
            self.customError(response)
        else:
            self.customSuccess(response)

    if 'acknowledge' in inputs:
        if inputs['acknowledge'] == True:
            time.sleep(18)
            responseAllAck = con.ackManagedDevicesAll()
            self.customSuccess(response="\n     All Devices Acknowledged\n")

def cli(argv: bytes=None) -> dict:
    """Args Parse for user input

    Args:
        argv (str, required): Apstra YAML Config File. Defaults to None.

    Returns:
        dict: Dict of args
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--filename',
                        required=True,
                        help='Apstra YAML Config File')

    args = parser.parse_args(argv)
    return args

def main():
    """Main callable function
    """    
    args=cli()
    yamlValidateFilename=yamlValidateFilePath()
    inputDict=loadYaml(filepath=args.filename)
    yamlValidate(inputDict, yamlValidateFilename)
    con=login(inputDict)
    inputProcess(inputDict, con)

if __name__ == "__main__":
    main()


