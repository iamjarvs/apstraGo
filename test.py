from jclClass import jclClass

x=jclClass()
x.login(password='admin', username='admin', port=39005, address='66.129.235.6')
#print(dir(x))
#print(help(x))
x.jclProvision(customerName='Pepsi')
