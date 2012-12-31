# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Website(Item):
    title = Field()
    url = Field()
    owned = Field() 
    status = Field()
    analytics = Field()
    pages = Field()

    def __str__(self):
      return "%s: url=%s,owned=%s,status=%s,analytics=%s" % (self.get('title'), self.get('url'), self.get('owned'), self.get('status'), self.get('analytics')) 

    def __wikitext_row__(self):
      return "a wikitext row representing this website"
