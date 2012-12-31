# Filename: dns_tools.py

import dns
import dns.name
import dns.query
import dns.resolver
from scrapy import log

def check_authority(url, nameservers):
    """check the list of authoritative nameservers for one of our canonical ones"""

    owned = 'N/A'

    # get a nameserver to resolve for us
    nameserver = '8.8.8.8' # Google's

    # create a dns name from the URL
    subject = dns.name.from_text(url)

    def query(nameserver, domain, response_type):
      """ generalize queries so we can do SOA, NS, etc; take params, return response """
      try:
        query = dns.message.make_query(domain, response_type)
        return dns.query.udp(query, nameserver, timeout=5)
      except:
        log.msg('Unable to lookup %s on %s: %s' % (url, nameserver, sys.exc_info()[0]), level=log.WARNING)
        # TODO: retry?

    response = query(nameserver, subject, dns.rdatatype.SOA)

    # handle some errors
    rcode = response.rcode()
    if rcode == dns.rcode.REFUSED:
      log.msg('Nameserver Error: %s refused to lookup %s.' % (nameserver, url), level=log.WARNING)
      return owned
    elif rcode == dns.rcode.NXDOMAIN:
      log.msg('Nameserver cannot find %s.' % url, level=log.DEBUG)
    elif rcode != dns.rcode.NOERROR:
      log.msg('Nameserver Error: while looking up %s received %s' % (url, dns.rcode.to_text(rcode)), level=log.WARNING)
      return owned

    # get the dns representation of the response
    ns = response.authority if len(response.authority) > 0 else response.answer
    # get the text representation of its first record
    ns = ns[0][0].to_text()
    # get the nameserver out of that
    ns = ns.split()[0].rstrip('.')

    # check if the ns is in our list of nameservers
    owned = ns in nameservers
    if owned: 
      log.msg('->Mozilla is authoritative for %s.' % (url), level=log.DEBUG)

    return owned

version = '0.1'
# end of modo


