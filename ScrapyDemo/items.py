# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class MovieItem(scrapy.Item):
    name=scrapy.Field()
    # 豆瓣网
    dianying = scrapy.Field()
    jianjies = scrapy.Field()
    pingfen = scrapy.Field()
    pingjia = scrapy.Field()
    # 58同城
    chengs=scrapy.Field()
    zhiwei=scrapy.Field()
    gongzi=scrapy.Field()
    daiyu=scrapy.Field()
    gsname=scrapy.Field()
    xueli=scrapy.Field()
    jingyan=scrapy.Field()
    # 58--保姆/护工
    nanny=scrapy.Field()


class ZuFang(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    address=scrapy.Field()
    rent=scrapy.Field()
    room=scrapy.Field()
    hall=scrapy.Field()
    area=scrapy.Field()
    orientations=scrapy.Field()
    subway=scrapy.Field()
    mode=scrapy.Field()
    note_one=scrapy.Field()
    note_two=scrapy.Field()
    note_three=scrapy.Field()
