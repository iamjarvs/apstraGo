import argparse
import pprint
from apstraGo.jclClass import jcl

def main(argv=None):
    """vLabs/JCL quick spinup
    """    

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-u', '--username',
                        required=True,
                        help='Apstra Username')

    parser.add_argument('-p', '--password',
                        required=True,
                        help='Apstra Password')

    parser.add_argument('-a', '--address',
                        required=True,
                        help='Apstra IP/DNS address')

    parser.add_argument('-v', '--port',
                        default=443,
                        help='Apstra http/https port number (default: %(default)s)')                                   

    parser.add_argument('-c', '--customer',
                        required=True,
                        help='Your Customers Name, use "for spaces" ')   

    args = parser.parse_args(argv)

    pprint.pprint(vars(args))

    asptraInstance = jcl()
    asptraInstance.login(username=args.username, password=args.password, address=args.address, port=args.port)

    asptraInstance.jclProvision(customerName=args.customer)

if __name__ == "__main__":
    main()