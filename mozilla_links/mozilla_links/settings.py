# Scrapy settings for mozilla_links project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'mozilla_links'

SPIDER_MODULES = ['mozilla_links.spiders']
NEWSPIDER_MODULE = 'mozilla_links.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mozilla_links (+http://www.yourdomain.com)'
