import scrapy
from ScrapyDemo.items import MovieItem
import re


class LiepinSpider(scrapy.Spider):
    name = 'LiePin'
    allowed_domains = ['liepin.com']
    start_urls = [
        'https://www.liepin.com/zhaopin/?compkind=&dqs=050040&pubTime=&pageSize=40&salary=&compTag=&sortFlag=15'
        '&degradeFlag=0&compIds=&subIndustry=&jobKind=&industries=&compscale=&key=%E9%87%91%E8%9E%8D&siTag'
        '=YPiarGk8ezW98-OjQBRhlg%7EER1bginubgxeQzYQLAUKgQ&d_sfrom=search_prime&d_ckId'
        '=f7ebabdbce82794e949702f719855758&d_curPage=1&d_pageSize=40&d_headId=f7ebabdbce82794e949702f719855758'
        '&curPage=0']
    custom_settings = {
        "RANDOM_DELAY": 5,
        "DOWNLOADER_MIDDLEWARES": {
            "project.middlewares.RandomDelayMiddleware": 999,
        }
    }
    cookie = {
        ' ':' '
    }

    def parse(self, response):
        uls = response.xpath('//div[@class="job-content"]//div[@class="sojob-result "]/ul[@class="sojob-list"]//li')
        for ul in uls:
            item = MovieItem()
            item['zhiwei'] = (ul.xpath(
                './div[@class="sojob-item-main clearfix"]//div[@class="job-info"]/h3/a//text)').extract_first()).strip()
            sal_edu_jingyan = ul.xpath(
                './div[@class="sojob-item-main clearfix"]//div[@class="job-info"]/p//span//text()').extract()
            self.SEJ(sal_edu_jingyan, item)
            item['chengs'] = ul.xpath(
                './div[@class="sojob-item-main clearfix"]//div[@class="job-info"]/p//a//text()').extract_first()
            item['gsname'] = (ul.xpath('./div[@class="sojob-item-main clearfix"]//div[@class="company-info '
                                       'nohover"]/p/a//text()').extract_first()).strip()
            daiyu = ul.xpath('./div[@class="sojob-item-main clearfix"]//div[@class="company-info nohover"]/p['
                             '@class="temptation clearfix"]//span//text()').extract()
            self.REdaiyu(daiyu, item)
            yield item

        next_urls = response.xpath('//div[@class="job-content"]//div[@class="sojob-result "]//div[@class="pager"]//div['
                                   '@class="pagerbar"]').extract()
        if next_urls:
            next_url = self.Next_Url(next_urls)
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, dont_filter=True, cookies=self.cookie)

    def SEJ(self, sal_edu_jingyan, item):
        item['gongzi'] = sal_edu_jingyan[0]
        item['xueli'] = sal_edu_jingyan[1]
        item['jingyan'] = sal_edu_jingyan[2]

    def REdaiyu(self, daiyu, item):
        if daiyu:
            item['daiyu'] = '、'.join(daiyu)
        else:
            item['daiyu'] = 'no'

    def Next_Url(self, next_urls):
        next_url = ''.join(next_urls)
        rex = r'<a href="(.*?)">(.*?)</a>'
        rex_url = r'&amp;'
        urls = re.findall(rex, next_url)
        data = str()

        for url in urls:
            if '下一页' in url:
                data = url[0]
        _url = re.sub(rex_url, r'&', data)
        return _url
