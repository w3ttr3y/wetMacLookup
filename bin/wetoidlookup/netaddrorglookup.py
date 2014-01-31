#!/usr/bin/env python

import netaddr

class NetaddrOrgLookup:
    
    def lookup(self, mac):
        try:
            x = netaddr.EUI(m)
            return ",".join([x.oui.registration(reg).org for reg in range(x.oui.reg_count)])
        except netaddr.core.AddrFormatError:
            return ""
        except netaddr.core.NotRegisteredError:
            return ""