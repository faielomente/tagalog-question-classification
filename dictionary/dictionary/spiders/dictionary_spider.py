import scrapy
from dictionary.items import DictionaryItem

class DictionarySpider(scrapy.Spider):
    name = 'dictionary'
    allowed_domains = ['tagalog.pinoydictionary.com']
    start_urls = [
        'http://tagalog.pinoydictionary.com/',
    ]

    def parse(self, response):
        # go through all the specified links
        for url in response.xpath('//a/@href').extract():
            if url.startswith('http://tagalog.pinoydictionary.com/word'):
                yield scrapy.Request(url, callback=self.parse_word)
            else:
                yield scrapy.Request(url, callback=self.parse)


    def parse_word(self, response):
        for sel in response.xpath('//div[@id="definition"]//dl'):
            item = DictionaryItem()
            item['word'] = sel.xpath('dt/a/text()').extract()
            item['tag'] = sel.xpath('dd/text()').extract()
            yield item