import scrapy
from ScrapyDemo.items import MovieItem


class MeijuSpider(scrapy.Spider):
    name='meiju'
    allowed_domains = ['mtime.com']
    start_urls = ['http://www.mtime.com/top/movie/top100_chinese/index.html']

    def parse(self,response):
        movies = response.xpath('//ul[@id="asyncRatingRegion"]/li')

        for each_movie in movies:
            item=MovieItem()
            item['name'] = each_movie.xpath('./div[@class="mov_pic"]/a/@title').extract()[0]
            yield item
        print("爬取成功")
