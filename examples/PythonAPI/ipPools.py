from apstraGo.apstraClass import apstra

def main():
    """This funtion perfoms a login & creates, shows and deletes an IP pool
    """    

    con = apstra()

    #Login and get API token
    con.login(password='admin', username='admin', port=443, address='192.168.1.81')
    
    #Print API Token
    print(con.apiToken)

    #Creat IP Pool
    con.resourceIpCreate(poolName='My_Test_Pool', network='10.0.0.0/24')

    #List all IP Pools
    allIpPools=con.resourceIpGet()
    print(allIpPools.json())

    #Delete IP Pool
    con.resourceIpDelete(poolName='My_Test_Pool')

if __name__ == "__main__":
    main()
