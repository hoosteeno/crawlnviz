crawlnviz
=========

a project to reimplement cmore's [crawler](https://github.com/chrismore/Domain-Name-Status-Checker) in python. 

goals:
  * maintainable
  * deployable to a variety of environments
  * pluggable data gathering/test framework
  * pluggable output format framework
  * maybe integrable with web server
  * goes to 11

it extends [scrapy](http://scrapy.org). 

running it right now will produce very little (and only in stdout) until there is more functionality. but you can run it:

    scrapy crawl moz


