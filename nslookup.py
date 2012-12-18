import dns
import dns.name
import dns.query
import dns.resolver

def mozilla_owns(d, log=lambda msg: None):
    domain = dns.name.from_text(d)
    nameservers = [
      'ns1.mozilla.org',
      'ns2.mozilla.org',
      'ns3.mozilla.org',
      'ns0.mozilla.or.jp,'
      'ns1.mozilla.net',
      'ns2.mozilla.net',
      'ns3.mozilla.net',
      'ns1.private.scl3.mozilla.com',
      'ns2.private.scl3.mozilla.com'
    ]

    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    log('Looking up %s' % (d))

    query = dns.message.make_query(domain, dns.rdatatype.NS)
    response = dns.query.udp(query, nameserver)

    rcode = response.rcode()
    if rcode != dns.rcode.NOERROR:
      if rcode == dns.rcode.NXDOMAIN:
        raise Exception('%s does not exist.' % d)
      else:
        raise Exception('Error %s' % dns.rcode.to_text(rcode))

    authoritative = response.answer[0][0].to_text().rstrip('.')

    mozilla_owns = authoritative in nameservers

    log('Mozilla is authoritative for %s? %s' % (d, mozilla_owns))

    return mozilla_owns

import sys

def log(msg):
    print msg

mozilla_owns(sys.argv[1], log)
