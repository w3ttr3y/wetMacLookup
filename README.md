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

As alternatives, the script can query http://api.macvendors.com/ just like TA-maclookup.  This is primarily intended for validating the results of the primary lookup. It can also utilize the netaddr module; in theory this would be better as it can return additional data, but in testing it doesn't return vendors as often (523 out of the 1,000 test cases vs 998 utilizing menuf)
 
