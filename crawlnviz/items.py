# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Website(Item):
    title = Field()
    url = Field()
    active = Field() 
    owned = Field() 

    def __str__(self):
        return "%s: owned=%s,active=%s" % (self.get('url'), self.get('owned'), self.get('active')) 

    def wikitext_row(self):
        return "a wikitext row representing this website"
