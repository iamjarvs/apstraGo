#!/usr/bin/python3
import argparse
import pprint
import jclClass


def main(argv=None):

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

    asptraInstance = jclClass.jclClass()
    asptraInstance.login(username=args.username, password=args.password, address=args.address, port=args.port)

    asptraInstance.jclProvision(customerName=args.customer)




if __name__ == "__main__":
    main()