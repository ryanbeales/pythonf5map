# Import
from collections import namedtuple
from lxml import html
from socket import gethostbyaddr

filehtml = None
with open('f5networkmap.html', 'r') as f:
    filehtml = f.read()

tree = html.fromstring(filehtml)

Service = namedtuple('service', ['virtual_server', 'pool', 'hosts'])
Host = namedtuple('host', ['address', 'vlan', 'port'])
services = list()

def format_service(s):
    return "{virtual_server}\n\t{pool}\n\t\t\t{hosts}\n".format(virtual_server=s.virtual_server, pool=s.pool, hosts=s.hosts)

for map in tree.xpath('//div[@class="map"]'):
    singleservice = dict()
    for element in map.getchildren():
        level = element.values()[0].strip()
        value = element.find('a').text_content().strip()

        if level in ['l1','l2']:
            singleservice[level] = value

        if level == 'l3':
            hostvalue = value.replace('%', ':').split(':')
            if value.find('%') > -1:
                host = Host(address=hostvalue[0], vlan=hostvalue[1], port=hostvalue[2])
            else:
                host = Host(address=hostvalue[0], vlan=None, port=hostvalue[1])

            if singleservice.has_key('l3'):
                singleservice[level].append(host)
            else:
                singleservice[level] = [host]

    s = Service(virtual_server=singleservice['l1'] if singleservice.has_key('l1') else None,
                pool=singleservice['l2'] if singleservice.has_key('l2') else None,
                hosts=singleservice['l3'] if singleservice.has_key('l3') else None)
    services.append(s)


# Output
def format_service(s):
    return "{virtual_server}\n\t{pool}\n\t\t\t{hosts}\n".format(virtual_server=s.virtual_server, pool=s.pool, hosts=s.hosts)

for s in services:
    print s
