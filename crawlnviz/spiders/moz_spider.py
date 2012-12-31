import sys
import re
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawlnviz.items import Website
import dns_tools

class MozSpider(BaseSpider):
  name = "moz"

  # TODO: move into cfg
  nameservers = {
    'ns.mozilla.org',
    'ns1.mozilla.org',
    'ns2.mozilla.org',
    'ns3.mozilla.org',
    'ns0.mozilla.or.jp',
    'ns.mozilla.net',
    'ns1.mozilla.net',
    'ns2.mozilla.net',
    'ns3.mozilla.net',
    'ns1.private.scl3.mozilla.com',
    'ns2.private.scl3.mozilla.com'
  }

  allowed_domains = ["mozilla.org"]

  start_urls = [
     "https://wiki.mozilla.org/Websites/Domain_List/http"
  ]

  def parse (self, response):
    websites = []
    hxs = HtmlXPathSelector(response)
    domains = hxs.select('//div[@id="main-content"]/ul/li/text()').extract()

    for domain in domains:
      website = Website(title="N/A", owned="N/A", status="N/A", analytics="N/A", pages="N/A")
      
      # assign the URL
      website['url'] = re.sub('\n', '', domain.strip())

      # set the owned flag
      try:
        website['owned'] = dns_tools.check_authority(website['url'], MozSpider.nameservers)
      except:
        log.msg('Unable to determine ownership of %s: %s' % (website['url'], sys.exc_info()[0]), level=log.WARNING)

      # TODO: set the status flag

      # TODO: set the analytics flag

      # TODO: populate pages
      
      # TODO: domain-level and page-level recursion

      websites.append(website)

    return websites


