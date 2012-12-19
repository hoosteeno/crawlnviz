# Filename: modo.py

import dns
import dns.name
import dns.query
import dns.resolver

from scrapy import log

def moz_nameservers():
    nameservers = {
      'ns1.mozilla.org': '',
      'ns2.mozilla.org': '',
      'ns3.mozilla.org': '',
      'ns0.mozilla.or.jp': '',
      'ns1.mozilla.net': '',
      'ns2.mozilla.net': '',
      'ns3.mozilla.net': '',
      'ns1.private.scl3.mozilla.com': '',
      'ns2.private.scl3.mozilla.com': ''
    }

    # use the default nameserver when looking up nameservers
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    for ns_name, ns_ip in nameservers.iteritems():
      # find the ip of the nameserver
      query = dns.message.make_query(ns_name, dns.rdatatype.A)
      response = dns.query.udp(query, nameserver, timeout=4)

      rcode = response.rcode()
      if rcode != dns.rcode.NOERROR:
        if rcode == dns.rcode.NXDOMAIN:
          log.msg('%s does not exist.' % (ns_name), level=log.WARNING)
        else:
          log.msg('Error %s' % (dns.rcode.to_text(rcode)), level=log.WARNING)

        continue 

      nameservers[ns_name] = (response.answer[0][0]).to_text()

      log.msg('%s has IP %s' % (ns_name, nameservers[ns_name]), level=log.DEBUG)

    # prune the list of nameservers -- no need to iterate on those we can't attach to
    nameservers = dict([(k,v) for k,v in nameservers.items() if len(v)>0])
    return nameservers

def moz_owned(url, nameservers):
    domain = dns.name.from_text(url)

    owned = False

    for ns_name, ns_ip in nameservers.iteritems():

      log.msg('Looking up %s on %s' % (url, ns_name), level=log.DEBUG)

      query = dns.message.make_query(domain, dns.rdatatype.NS)
      response = dns.query.udp(query, ns_ip, timeout=4)

      rcode = response.rcode()
      if rcode != dns.rcode.NOERROR:
        if rcode == dns.rcode.REFUSED:
          continue
        if rcode == dns.rcode.NXDOMAIN:
          raise Exception('%s does not exist.' % url)
        else:
          raise Exception('Error %s' % dns.rcode.to_text(rcode))

      rns = response.answer[0][0].to_text().rstrip('.')
      if rns == ns_name:
        owned = True
        log.msg('->Mozilla is authoritative for %s.' % (url), level=log.DEBUG)
        break

    return owned

version = '0.1'
# end of modo


