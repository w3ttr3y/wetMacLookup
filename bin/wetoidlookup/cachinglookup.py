#!/usr/bin/env python

class cachingLookup:
    cache = {}
    
    def __init__(self, lookup):
        self.lookupfun = lookup
        
    def lookup(self, mac):
        if self.cache.has_key(mac):
            return self.cache[mac]
        else:
            vendor = self.lookupfun(mac)
            self.cache[mac] = vendor
            return vendor
 
if __name__ == '__main__':
    cache = cachingLookup(lambda x: "Apple")
    cache.lookup("00:de:ad:be:ef:00")
    cache.lookup("00:de:ad:be:ef:00")
    cache.lookup("11:de:ad:be:ef:11")
    cache.lookup("00:de:ad:be:ef:00")
    cache.lookup("11:de:ad:be:ef:11")
    