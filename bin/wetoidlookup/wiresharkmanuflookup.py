#!/usr/bin/env python

import re

class WiresharkOIDLookup:
    wsRx = re.compile(r"(?P<mac_prefix>[0-9a-fA-F:.-]+)(?:/(?P<mac_mask>\d+))?\s+(?:(?P<vendor>\S+)\s*(?P<comment>#.*)?$)?(?:(?P<vendor2>.+)\s*$)?")
    macRx = re.compile(r"[a-f0-9]{2}")
    lookups = {}
    
    def parseMac(self, mac):
        # Not efficient, but it gets the job done
        mac = mac.replace(':','')
        mac = mac.replace('-','')
        mac = mac.replace('.','')
        mac = '{:0<12}'.format(mac)
        return int(mac, 16)
    
    def makeMask(self, bits, size):
        bits = int(bits)
        size = int(size)
        return ((2L<<int(bits)-1) - 1)<<(size-bits)
    
    def parseLine(self, line):
        m = self.wsRx.match(line)
        if m is not None:
            prefix = m.group('mac_prefix')
            bits = m.group('mac_mask')
            
            # Most of the time vendor doesn't have spaces, but in a couple of cases it does
            # which threw off my regex.  I should rewrite, but instead I just append a vendor2
            vendor = m.group('vendor')
            if vendor is None:
                vendor = m.group('vendor2')
                if vendor is None:
                    vendor = 'Unknown'
            
            comment = m.group('comment')
            
            if bits is None:
                bits = 4 * (len(prefix) - len(prefix) / 3)
            
            mac = self.parseMac(prefix)
            mask = self.makeMask(bits, 48)
            return (mac, mask, vendor, comment)
        #else:
        #    print "line didn't match: %s" % (line)

    def loadFile(self, lookupFile):
        try:
            with open(lookupFile) as file:
                for line in file:
                    if line[0] == "#":
                        continue
                    items = self.parseLine(line)
                    if items is not None:
                        (mac, mask, vendor, comment) = items
                        if mask in self.lookups:
                            self.lookups[mask][mac] = (vendor, comment)
                        else:
                            self.lookups[mask] = {mac: (vendor,comment)}
        except IOError:
            import os
            if not os.path.exists(lookupFile):
                import urllib
                urllib.urlretrieve ("http://anonsvn.wireshark.org/wireshark/trunk/manuf", lookupFile)
                self.loadFile(lookupFile)
        
    def lookup(self, mac):
        if self.lookups is None:
            return
        mac = self.parseMac(mac)
                
        for netmask in self.lookups:
            m = mac & netmask
            if self.lookups[netmask].has_key(m):
                return self.lookups[netmask][m][0]

if __name__ == '__main__':
    #foo = WiresharkOIDLookup()
    print os.path.join(os.path.dirname(__file__), '../usr/manuf')
    #foo.loadFile(os.path.join(os.path.dirname(__file__), '../usr/manuf'))
    #for mac in ["68:5b:35:7b:16:ed", "a8:bb:cf:1d:4b:76", "d2:00:1a:01:05:40"]:
    #    print "%s: %s" % (mac, foo.lookup(mac))
