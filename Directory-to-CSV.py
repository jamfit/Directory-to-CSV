import argparse
from collections import OrderedDict
import csv
import getpass
import ldap
import os
import sys


def arg_parser():
    attributes = OrderedDict()
    attributes['name'] = 'Full Name'
    attributes['mail'] = 'Email'
    attributes['telephoneNumber'] = 'Phone Number'

    parser = argparse.ArgumentParser(
        prog="Directory to CSV",
        description="Create a CSV output of accounts in an LDAP OU",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""
The default attributes are: name: 'Full Name', mail: 'Email', telephoneNumber: 'Phone Number'
Define a CSV file by passing LDAP attributes as arguments
Set a label for the argument by passing a value after a colon

The output csv file's columns will have the same order as the passed attributes

Example usage:
$ ./directory-to-csv.py
$ ./directory-to-csv.py  "name:Full Name" mail
 """)

    parser.add_argument('attributes', nargs='*', help="Additional attributes to read from LDAP records")
    parser.add_argument('-o', '--output', type=str, dest='output', help="Path to write CSV (default current dir)",
                        default='{}/directory.csv'.format(os.getcwd()))

    args = parser.parse_args()

    if args.attributes:
        new_attributes = OrderedDict()
        for a in args.attributes:
            a = a.split(':')
            #new_attributes[a[0]] = '' if len(a) == 1 else new_attributes[a[0]] = a[1]
            if len(a) == 1:
                new_attributes[a[0]] = a[0]
            else:
                new_attributes[a[0]] = a[1]

        attributes = new_attributes

    return attributes, args.output


class LDAPs:
    def __init__(self, server, account, password, staff_ou):
        # Force ldap to use SSL and not TLS for connections
        self.staff_ou = staff_ou
        self.account = 'CN={0},{1}'.format(account, self.staff_ou)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.l = ldap.initialize(server)
        self.bind(password)

    def bind(self, password):
        try:
            self.l.simple_bind_s(self.account, password)
        except ldap.INVALID_CREDENTIALS:
            print("Invalid credentials")
            sys.exit(1)
        except ldap.SERVER_DOWN:
            print("Server unavailable")
            sys.exit(1)

    def staff_accounts(self, dn=None, flter='(cn=*)', attrs=None):
        if not dn:
            dn = self.staff_ou

        results = self.l.search_s(dn, ldap.SCOPE_ONELEVEL, filterstr=flter, attrlist=attrs)
        results.sort()
        return results

    def unbind(self):
            self.l.unbind_s()


def write_csv(file_path, attribute_dict, ldap_list):
    with open(file_path, 'w') as f:
        print("Writing CSV file to: {}".format(f.name))
        csv_file = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        csv_file.writerow([key[1] for key in attribute_dict.iteritems()])
        for i in ldap_list:
            new_line = list()
            for key in attribute_dict:
                try:
                    new_line.append(i[1][key][0])
                except KeyError:
                    new_line.append('')

            csv_file.writerow(new_line)


def main():
    ldap_server = None
    ldap_account = None
    ldap_password = None
    # The staff OU that wil be used (it is assumed the authenticating user resides in this OU)
    staff_ou = 'OU=Staff,DC=yourorg,DC=corp'

    attributes, file_path = arg_parser()
    print("LDAP attributes to search and map to CSV column:")
    print_attrs = list()
    for key, value in attributes.iteritems():
        print_attrs.append('{}: {}'.format(key, value))

    print(', '.join(print_attrs))

    if not ldap_server:
        ldap_server = str(raw_input("LDAP Server: "))
        if not ldap_server.startswith('ldaps://'):
            ldap_server = 'ldaps://{}'.format(ldap_server)

    if not ldap_account:
        ldap_account = str(raw_input("LDAP User(CN): "))

    if not ldap_password:
        ldap_password = getpass.getpass("Password: ")

    l = LDAPs(ldap_server, ldap_account, ldap_password, staff_ou)

    print("Reading accounts in {} in LDAP".format(l.staff_ou))
    staff_list = l.staff_accounts(attrs=[key for key in attributes])
    l.unbind()

    write_csv(file_path, attributes, staff_list)
    print("Done\n")

if __name__ == '__main__':
    main()