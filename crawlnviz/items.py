# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MozillaLinksItem(Item):
    title = Field()
    url = Field()
    live = Field() #bool: is the link live?