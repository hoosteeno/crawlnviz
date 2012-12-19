# Filename: modo.py
# TODO: make it more general (names, cfg, etc)

import dns
import dns.name
import dns.query
import dns.resolver

from scrapy import log

## 
# check if the list of nameservers includes a nameserver that is authoritative for the url 
##
def moz_nameservers():
    # TODO: move this into cfg 
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

    # TODO: DRY this below
    # foreach nameserver in our list
    for ns_name, ns_ip in nameservers.iteritems():
      # find the ip of the nameserver
      query = dns.message.make_query(ns_name, dns.rdatatype.A)
      try:
        response = dns.query.udp(query, nameserver, timeout=4)
      except:
        log.msg('Unable to lookup %s on %s: %s' % (url, ns_name, sys.exc_info()[0]), level=log.WARNING)
        continue

      rcode = response.rcode()
      if rcode != dns.rcode.NOERROR:
        if rcode == dns.rcode.REFUSED:
          log.msg('Nameserver Error: %s refused lookup.' % ns_name, level=log.WARNING)
        elif rcode == dns.rcode.NXDOMAIN:
          log.msg('Nameserver Error: %s does not exist.' % ns_name, level=log.WARNING)
        else:
          log.msg('Nameserver Error: %s' % dns.rcode.to_text(rcode), level=log.WARNING)
        continue 

      # assign the IP we found
      nameservers[ns_name] = (response.answer[0][0]).to_text()
      log.msg('%s has IP %s' % (ns_name, nameservers[ns_name]), level=log.DEBUG)

    # prune the list of nameservers -- no need to iterate on those we can't attach to
    nameservers = dict([(k,v) for k,v in nameservers.items() if len(v)>0])

    return nameservers

## 
# check if the list of nameservers includes a nameserver that is authoritative for the url 
##
def moz_owned(url, nameservers):

    # create a dns name from the URL
    domain = dns.name.from_text(url)

    owned = False

    # TODO: DRY this above
    for ns_name, ns_ip in nameservers.iteritems():

      log.msg('Looking up %s on %s (%s)' % (url, ns_name, ns_ip), level=log.DEBUG)

      # lookup the on this nameserver
      query = dns.message.make_query(domain, dns.rdatatype.NS)
      try:
        response = dns.query.udp(query, ns_ip, timeout=5)
      except:
        log.msg('Unable to lookup %s on %s: %s' % (url, ns_name, sys.exc_info()[0]), level=log.WARNING)
        continue

      rcode = response.rcode()
      if rcode != dns.rcode.NOERROR:
        if rcode == dns.rcode.REFUSED:
          log.msg('Nameserver Error: %s refused lookup.' % ns_name, level=log.WARNING)
        elif rcode == dns.rcode.NXDOMAIN:
          log.msg('Nameserver Error: %s does not exist.' % ns_name, level=log.WARNING)
        else:
          log.msg('Nameserver Error: %s' % dns.rcode.to_text(rcode), level=log.WARNING)
        continue 

      # we got a nameserver here
      rns = response.answer[0][0].to_text().rstrip('.')
  
      # TODO: fix. this is not an adequate test of authority.
      if rns == ns_name:
        owned = True
        log.msg('->Mozilla is authoritative for %s.' % (url), level=log.DEBUG)
        break

    return owned

version = '0.1'
# end of modo


