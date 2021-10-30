import scrapy
from ScrapyDemo.items import MovieItem


class TongchengNannySpider(scrapy.Spider):
    name = 'Tongcheng_nanny'
    allowed_domains = ['dg.58.com']
    start_urls = [
        'https://dg.58.com/job/pn2/?key=%E6%8A%A4%E5%B7%A5&final=1&jump=1&PGTID=0d302408-0019-db8a-74a3-197a7ee4cb51'
        '&ClickID=3']

    def parse(self, response):
        nannys = response.xpath('//*[@id="list_con"]')
        for nanny in nannys:
            item = MovieItem()
            item['nanny'] = nanny.xpath('/li[1]/div[1]/p')
