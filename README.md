Vendor Lookup for MAC Address
============
This Add-on adds a script lookup to enable you to lookup the vendor of a MAC address (also known as hardware or physical address) as is common in the IEEE 802 standards.

History
============
My day job is supporting a decent size installation of Splunk and a coupld weeks ago one of our parttime employees was working on a script to look up the vendors of mac addresses.  Once I started thinking about it, I honestly was a bit surprised this wasn't built in.

I looked on Splunk Apps (http://apps.splunk.com) and all I found was a TA-maclookup (http://apps.splunk.com/app/1249/).  My concern with TA-maclookup was it uses an online lookup which would have significant latency and thus wouldn't scale to large numbers of mac addresses. In a very unscientific, one run (and thus invalid) test, 1,000 mac addresses took 4.5 minutes to return their vendor.

Overview
============
maclookup.py is a python script which reads in a csv file over stdin and outputs a csv file to stdout.  The first version of this script was able to process over 1,000 mac address in under .3 seconds (again unscientific, one run and thus invalid) and further improvements could be made.  Thus, this script seems much better suited for use in situations where large numbers of addresses may be looked up or if you have impatient users :-)

The script starts by reading in a file called manuf; it is obtained from the Wireshark project (http://www.wireshark.org) and newer versions can be downloaded from http://anonsvn.wireshark.org/wireshark/trunk/manuf  The file utilizes IEEE public OUI listing and Michael Patton's "Ethernet Codes Master Page" so it may not always return what you might assume it should, but in practice it should be a bit more accurate.

As alternatives, the script can query http://api.macvendors.com/ just like TA-maclookup.  This is primarily intended for validating the results of the primary lookup. It can also utilize the netaddr module (https://pypi.python.org/pypi/netaddr/); in theory this would be better as it can return additional data, but in testing it doesn't return vendors as often (523 out of the 1,000 test cases vs 998 utilizing menuf)

Usage (outside of Splunk)
============
In general the script reads a csv file on stdin and outputs one on stdout.  Since it doesn't require headers, a real simple test would be:

    echo "68:5b:35:7b:16:ed" | bin/maclookup.py
which should return:

    68:5b:35:7b:16:ed,Apple

The script also comes with two sample csv files in the samples directory: macs1000.csv and macs10000.csv with 1,000 and 10,000 test records respectively (there may be overlap between the two files but shouldn't be within).

    cat samples/macs1000.csv  | bin/maclookup.py
    cat samples/macs10009.csv | bin/maclookup.py
    
The script can also accept several arguments, including -h for help

    python-dev$ bin/maclookup.py -h
    usage: maclookup.py [-h] [-c] [-l LOOKUP] [-n] [-r]

    Make a best guess towards the vendor of a network card based upon its MAC (physical) address

    optional arguments:
      -h, --help            show this help message and exit
      -c, --cache           Cache the addresses that have been looked up (only makes sense if address repeat often)
      -l LOOKUP, --lookup LOOKUP
                            Change the lookup function Options: wireshark
                            (default), macvendorscom, netaddr
      -n, --no-network      Prevents librariest from downloading required files
                            from network (e.g. if manuf is not present, it can be
                            automatically downloaded)
      -r, --readonly        Turns on readonly mode so that the program will not
                            usr local files to cache lookups between runs.
