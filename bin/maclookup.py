#!/usr/bin/env python

import os
import sys

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

def createLookup(library=None):
    if(library == "netaddr"):
        import wetoidlookup.netaddrorglookup
        lookup = wetoidlookup.NetaddrOrgLookup()
    elif(library == "macvendorscom"):
        import wetoidlookup.remotemacvendorscomlookup
        lookup = wetoidlookup.remotemacvendorscomlookup()
    else:
        import wetoidlookup.wiresharkmanuflookup as wiresharkmanuflookup
        ws2 = wiresharkmanuflookup.WiresharkOIDLookup()
        ws2.loadFile(os.path.join(os.path.dirname(__file__), '../var/manuf'))
        lookupfunc =  lambda m: ws2.lookup(m)
    return lookupfunc
        
def createIO():
    import wetoidlookup.myio
    return wetoidlookup.myio.MyIO()

def createAppender(generator, lookup):
    import wetoidlookup.appendrecord
    return wetoidlookup.appendrecord.AppendRecord(generator, lookup)

def createCache(lookupfunc):
    #try to add a really primitive cache
    import wetoidlookup.cachinglookup
    cache = wetoidlookup.cachinglookup.cachingLookup(lookupfunc)
    return lambda m: cache.lookup(m)
    
if __name__ == '__main__':
    cache = None
    lookupfunc = createLookup()
    
    if cache:
        lookupfunc = createCache(lookupfunc)
        
    ioHandler = createIO()    
    recordAppender = createAppender(lambda: ioHandler.readCSV(sys.stdin), lookupfunc)
    
    for record in recordAppender.process():
        if record is not None:
            ioHandler.writeCSV(record)