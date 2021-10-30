import scrapy
from ScrapyDemo.items import MovieItem
import re


class TongchengMoneySpider(scrapy.Spider):
    name = 'TongCheng_money'
    allowed_domains = ['dg.58.com']
    start_urls = ['https://dg.58.com/job/?key=%E9%87%91%E8%9E%8D&classpolicy=job_B,'
                  'uuid_8425b1f714b949d6881a34fa45906d54,displocalid_413,from_9224,to_jump&final=1']
    custom_settings = {
        "RANDOM_DELAY": 5,
        "DOWNLOADER_MIDDLEWARES": {
            "project.middlewares.RandomDelayMiddleware": 999,
        }
    }
    cookie={
        '':'',
    }

    def parse(self, response):
        uls=response.xpath('//div[@class="leftCon"]//ul[@id="list_con"]//li[@class="job_item clearfix"]')

        for ul in uls:
            item = MovieItem()
            chengs_gangwei=''.join(ul.xpath('.//div[@class="job_name clearfix"]/a//text()').extract())
            self.rechengs(chengs_gangwei,item)

            item['gongzi']=ul.xpath('.//p[@class="job_salary"]//text()').extract_first()        #工资
            item['gsname']=ul.xpath('.//div[@class="comp_name"]/a//text()').extract_first().strip()

            zhiwei_yaoqiu=ul.xpath('.//p[@class="job_require"]//span//text()').extract()
            self.ZhiWei_YaoQiu(zhiwei_yaoqiu,item)
            daiyu=ul.xpath('.//div[@class="job_wel clearfix"]//text()').extract()
            self.re_daiyu(daiyu,item)
            gsname_yaoqiu=ul.xpath('.//div[@class="item_con job_comp"]//text()').extract()

            yield item

        next_urls=response.xpath('.//div[@class="leftCon"]//div[@class="pagesout"]//a[@class="next"]/@href').extract_first()

        if next_urls:
            yield scrapy.Request(next_urls, callback=self.parse,cookies=self.cookie)

    # 分解城区和岗位
    def rechengs(self,chengs_gangwei,item):
        rex="\|"
        data=re.split(rex,chengs_gangwei)
        item['chengs']=data[0].strip()

    # 分解待遇
    def re_daiyu(self,daiyu,item):
        if daiyu:
            new_daiyu=''.join(daiyu)
            item['daiyu'] = re.sub('   ', '+', new_daiyu.strip())
        else:
            item['daiyu']='no'

    # 分级岗位和要求
    def ZhiWei_YaoQiu(self,zhiwiei,item):
        item['zhiwei']=zhiwiei[0].strip()
        item['xueli']=zhiwiei[1].strip()
        item['jingyan']=zhiwiei[2].strip()



