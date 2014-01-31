#!/usr/bin/env python

import os
import sys

def createLookup(library=None, network=True, readonly=False):
    if(library == "netaddr"):
        import wetoidlookup.netaddrorglookup
        lookup = wetoidlookup.NetaddrOrgLookup()
    elif(library == "macvendorscom"):
        #TODO: if network = False then throw an error
        import wetoidlookup.remotemacvendorscomlookup
        lookup = wetoidlookup.remotemacvendorscomlookup.RemoteMacvendorsComLookup()
    else:
        import wetoidlookup.wiresharkmanuflookup as wiresharkmanuflookup
        lookup = wiresharkmanuflookup.WiresharkOIDLookup(network, readonly)
        #lookup.loadFile(os.path.join(os.path.dirname(__file__), '../var/manuf'))
        # Pickling is actually slower then parsing the text file out of the box
        # using cPickle and version 2 is about half as faster.  At .1 seconds, I'm not convinced
        # its worth it given that pickling could lead to a security issue if the file is maliciously modified
        lookup.loadPickleFile(os.path.join(os.path.dirname(__file__), '../var/manuf.p'), 2)
    return lookup
        
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
    import argparse
    parser = argparse.ArgumentParser(description='Make a best guess towards the vendor of a network card based upon its MAC (physical) address')
    parser.add_argument('-c', '--cache', dest='cache', action='store_const', const=True, default=False,
                        help='Cache the addresses that have been looked up (only makes sense if address repeat often)')    
    parser.add_argument('-l', '--lookup', default='wiresharkmanuf', type=str,
                   help='Change the lookup function Options: wireshark (default), macvendorscom, netaddr')
    parser.add_argument('-n', '--no-network', dest='network', action='store_const', const=True, default=False,
                        help="Prevents librariest from downloading required files from network (e.g. if manuf is not present, it can be automatically downloaded)")
    parser.add_argument('-r', '--readonly', dest='readonly', action='store_const', const=True, default=False,
                        help="Turns on readonly mode so that the program will not usr local files to cache lookups between runs.")

    args = parser.parse_args()
    lookupfunc = createLookup(args.lookup, not args.network, args.readonly)
    
    if args.cache:
        lookupfunc = createCache(lookupfunc)
        
    ioHandler = createIO()    
    recordAppender = createAppender(lambda: ioHandler.readCSV(sys.stdin), lambda m: lookupfunc.lookup(m))
    
    try:
        for record in recordAppender.process():
            if record is not None:
                ioHandler.writeCSV(record)
    #TODO: trying to fix the problem of printing error messages when piped to head, but the fix isn't working.
    except IOError:
        try:
            sys.stdout.close()
        except IOError:
            pass
        try:
            sys.stderr.close()
        except IOError:
            pass