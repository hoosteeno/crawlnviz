# Filename: modo.py
# TODO: make it more general (names, cfg, etc)

import dns
import dns.name
import dns.query
import dns.resolver

from scrapy import log

## 
# check the list of authoritative nameservers for one of our canonical ones
##
def authoritative(url, nameservers):

    # get a nameserver to resolve for us
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    # create a dns name from the URL
    domain = dns.name.from_text(url)

    owned = False

    # ask for the list of authoritative nameservers for the domain
    query = dns.message.make_query(domain, dns.rdatatype.NS)
    try:
      response = dns.query.udp(query, nameserver, timeout=5)
    except:
      log.msg('Unable to lookup %s on %s: %s' % (url, nameserver, sys.exc_info()[0]), level=log.WARNING)
      # TODO: retry?

    # handle some errors
    rcode = response.rcode()
    if rcode != dns.rcode.NOERROR:
      if rcode == dns.rcode.REFUSED:
        log.msg('Nameserver Error: %s refused to lookup %s.' % (nameserver, url), level=log.WARNING)
      elif rcode == dns.rcode.NXDOMAIN:
        log.msg('Nameserver Error: server cannot find %s.' % url, level=log.WARNING)
      else:
        log.msg('Nameserver Error: while looking up %s received %s' % (url, dns.rcode.to_text(rcode)), level=log.WARNING)
      return owned

    # for every nameserver in the response...
    for rns in response.answer[0]:
      rns = rns.to_text().rstrip('.')
      
      # check to see if it's in our canonical list
      owned = rns in nameservers
      if owned: 
        log.msg('->Mozilla is authoritative for %s.' % (url), level=log.DEBUG)
        break

    return owned

version = '0.1'
# end of modo


