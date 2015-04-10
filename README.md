# Directory to CSV

## What were we trying to solve?

We needed a quick way to dump the contents of our staff accounts in AD into a CSV list with different values extracted depending on what the list was to be used for. For example: in order to update Envoy we must upload a CSV file of users containing their "Full Name", "Email" and "Phone Number" with matching headers for the columns.

## What does it do?

When run, the script will prompt for the address to an LDAP server and then for credentials. The distinguished name (DN) of the OU is hardcoded inside the main() function (you can also optionally hard code the other values for LDAP server address and credentials there).

## How to use this script

This Python script can be run on Mac, Linux and Windows (Python version 2.7.x tested). The script requires the "python-ldap" module which you can install on your system or in a virtual environment using the requirements.txt file.

```
pip install -r /path/to/requirements.txt
``` 

By default the three attributes it populates into the CSV file are name, mail and telephoneNumber (these as AD attributes). To output a CSV with your own selected attributes, pass them as arguments to the script. To set the custom text of the column header, have it follow the attribute separated be a colon ':'.
You can also run the script with the -h argument to view the help text:

```
usage: Directory to CSV [-h] [-o OUTPUT] [attributes [attributes ...]]
Create a CSV output of accounts in an LDAP OU

positional arguments:
 attributes Additional attributes to read from LDAP records

optional arguments:
 -h, --help show this help message and exit
 -o OUTPUT, --output OUTPUT
            Path to write CSV (default current dir)

The default attributes are: name: 'Full Name', mail: 'Email', telephoneNumber: 'Phone Number'
Define a CSV file by passing LDAP attributes as arguments
Set a label for the argument by passing a value after a colon

The output csv file's columns will have the same order as the passed attributes

Example usage:
$ ./directory-to-csv.py
$ ./directory-to-csv.py "name:Full Name" mail
```

## License

```
JAMF Software Standard License

Copyright (c) 2015, JAMF Software, LLC. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of
      conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.
    * Neither the name of the JAMF Software, LLC nor the names of its contributors may be
      used to endorse or promote products derived from this software without specific prior
      written permission.

THIS SOFTWARE IS PROVIDED BY JAMF SOFTWARE, LLC "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JAMF SOFTWARE, LLC BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
