#!/usr/bin/env python

import netaddr
import sys
import string

def getWiresharkOrg3(foo, m):
    if m == "mac":
        return
    return foo.lookup(m)

def getNetaddrOrgs(m):
    try:
        x = netaddr.EUI(m)
        return ",".join([x.oui.registration(reg).org for reg in range(x.oui.reg_count)])
    except netaddr.core.AddrFormatError:
        return ""
    except netaddr.core.NotRegisteredError:
        return ""

def getRemoteOrgs(m):
    import urllib
    url = "http://api.macvendors.com/"
    url = "%s%s" % (url, m)
    f = urllib.urlopen(url)
    return f.read()

def getWiresharkOrg(m):
    import urllib
    file = urllib.urlopen("http://anonsvn.wireshark.org/wireshark/trunk/manuf")
    data = file.readlines()
    oui = m[0:8].upper()
    max = len(data)
    for x in range(0,max):
        if oui in data[x]:
            return data[x]

def getWiresharkOrg2(m):
    try:
        with open('manuf') as file:
            data = file.readlines()
            oui = m[0:8].upper()
            max = len(data)
            for x in range(0,max):
                if oui in data[x]:
                    return data[x]
    except IOError:
        import os
        if not os.path.exists('manuf'):
            import urllib
            file = urllib.urlopen("http://anonsvn.wireshark.org/wireshark/trunk/manuf")
            getWiresharkOrg2(m)

class MyIO:
    headers = []
 
    def readCSV2(self, stream, func):
        headers = [h.strip() for h in string.split(next(stream), ",")]
    
        #yield headers
    
        for line in stream:
            line = line.strip()
            mac = "or ".join(func(line))
            yield [line, mac]

    def readCSV(self, stream):
        headers = [h.strip() for h in string.split(next(stream), ",")]
    
        yield headers
        for line in stream:
            yield [line.strip()]

    def escapeRecords(self, records):
        return [ "" if record is None else
                "\"%s\"" % record if "," in record else
                record for record in records]

    def writeCSV(self, records):
        if records is not None:
            escapedRecords = self.escapeRecords(records) 
            if escapedRecords is not None:
                print ",".join(escapedRecords)

class AppendRecord:
    lookup = lambda x: x
    gen = None
    
    def __init__(self, generator, lookupFunction):
        self.gen = generator
        self.lookup=lookupFunction

    def process(self):
        for record in self.gen():
            record.append(self.lookup(record[0]))
            yield record

if __name__ == '__main__':
    #lookupfunc = getNetaddrOrgs
    lookupfunc = getRemoteOrgs
    #lookupfunc = getWiresharkOrg
    #lookupfunc = getWiresharkOrg2
    
    #import wiresharkmanuflookup
    #ws = wiresharkmanuflookup.WiresharkOIDLookup()
    #ws.loadFile("manuf")
    #lookupfunc =  lambda m: getWiresharkOrg3(ws, m)
    
    #import wiresharkmanuflookup2
    #ws2 = wiresharkmanuflookup2.WiresharkOIDLookup()
    #ws2.loadFile("manuf")
    #lookupfunc =  lambda m: getWiresharkOrg3(ws2, m)
    
    #try to add a really primitive cache
    import cachinglookup
    cache = cachinglookup.cachingLookup(lookupfunc)
    lookupfunc = lambda m: cache.lookup(m)
    
    foo = MyIO()    
    bar = AppendRecord(lambda: foo.readCSV(sys.stdin), lookupfunc)
    for record in bar.process():
        if record is not None:
            foo.writeCSV(record)
