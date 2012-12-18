from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawlnviz.items import MozillaLinksItem
import re

class MozSpider(BaseSpider):
  name = "moz"

  allowed_domains = ["mozilla.org"]

  start_urls = [
     "https://wiki.mozilla.org/Websites/Domain_List/Mozilla_Prod_Owned_Root_Domains"
  ]

  # ultimately parse will call 2 functions: one to get all the domains, one to handle all the domains
  def (self, response):
    items = []
    hxs = HtmlXPathSelector(response)
    domains = hxs.select('//div[@id="main-content"]/ul/li/text()').extract()

    for domain in domains:
      item = MozillaLinksItem()
      item['url'] = re.sub('\n', '', domain.strip())
      items.append(item)

      if len(MozSpider.allowed_domains) == 1:
        MozSpider.allowed_domains.append(item['url'])

    return items


