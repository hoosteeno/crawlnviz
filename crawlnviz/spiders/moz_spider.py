from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawlnviz.items import MozillaLinksItem
import re
import modo

class MozSpider(BaseSpider):
  name = "moz"

  nameservers = modo.moz_nameservers()

  allowed_domains = ["mozilla.org"]

  start_urls = [
     "https://wiki.mozilla.org/Websites/Domain_List/Mozilla_Prod_Owned_Root_Domains"
  ]

  def parse (self, response):
    items = []
    hxs = HtmlXPathSelector(response)
    domains = hxs.select('//div[@id="main-content"]/ul/li/text()').extract()

    for domain in domains:
      item = MozillaLinksItem()
      item['url'] = re.sub('\n', '', domain.strip())
      #try:
      item['owned'] = modo.moz_owned(item['url'], MozSpider.nameservers)
      #except:
        #pass
      items.append(item)

    return items


