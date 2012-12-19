from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawlnviz.items import Website
import sys
import re
import modo

class MozSpider(BaseSpider):
  name = "moz"

  # TODO: move into cfg
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

  allowed_domains = ["mozilla.org"]

  start_urls = [
     "https://wiki.mozilla.org/Websites/Domain_List/Mozilla_Prod_Owned_Root_Domains"
  ]

  def parse (self, response):
    items = []
    hxs = HtmlXPathSelector(response)
    domains = hxs.select('//div[@id="main-content"]/ul/li/text()').extract()

    for domain in domains:
      item = Website()
      item['url'] = re.sub('\n', '', domain.strip())
      try:
        item['owned'] = modo.authoritative(item['url'], MozSpider.nameservers)
      except:
        item['owned'] = "N/A"
      items.append(item)

    return items


