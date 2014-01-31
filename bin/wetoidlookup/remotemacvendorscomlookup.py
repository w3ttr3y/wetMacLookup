#!/usr/bin/env python

import urllib

class RemoteMacvendorsComLookup(object):

    def lookup(self, mac):
        url = "http://api.macvendors.com/"
        url = "%s%s" % (url, mac)
        f = urllib.urlopen(url)
        return f.read()