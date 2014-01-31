#!/usr/bin/env python

try:
    import netaddr
except ImportError:
    import sys
    sys.stderr.write("Unable to import netaddr library.  You may need to download it. https://pypi.python.org/packages/source/n/netaddr/netaddr-0.7.10.tar.gz#md5=605cfd09ff51eaeff0ffacdb485e270b")
    raise

class NetaddrOrgLookup:
    
    def lookup(self, mac):
        try:
            x = netaddr.EUI(m)
            return ",".join([x.oui.registration(reg).org for reg in range(x.oui.reg_count)])
        except netaddr.core.AddrFormatError:
            return ""
        except netaddr.core.NotRegisteredError:
            return ""