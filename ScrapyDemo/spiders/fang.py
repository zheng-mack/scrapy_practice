import scrapy
from ScrapyDemo.items import ZuFang
import re


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['gz.zu.fang.com']
    cookies = {'global_cookie': '  ',
               'city': 'gz',
               }

    def start_requests(self):
        url = 'https://gz.zu.fang.com/'
        yield scrapy.Request(url, callback=self.parse, cookies=self.cookies, dont_filter=True)

    def parse(self, response):
        dls = response.xpath('//div[@class="houseList"]//dl[@class="list hiddenMap rel listGray"]')
        for dl in dls:
            item = ZuFang()

            item['name'] = dl.xpath('.//p[@class="title"]//a/text()').extract_first().strip()
            item['address'] = dl.xpath('.//p[@class="gray6 mt12"]//a//text()').extract_first().strip()
            item['rent'] = int(dl.xpath('.//p[@class="mt5 alingC"]/span//text()').extract_first().strip())
            font15_mt12_bold = dl.xpath('.//p[@class="font15 mt12 bold"]//text()').extract()
            self.font_mt_bold(font15_mt12_bold, item)

            subway = dl.xpath(
                './/dd[@class="info rel"]//p[@class="mt12"]//span[@class="note subInfor"]//project()').extract()
            self.Subway(subway, item)

            note = dl.xpath('.//dd[@class="info rel"]/p[@class="mt12"]//project()').extract()
            self.NoteF(note, item)
            print(item)
            yield item

        next_starturl = response.xpath('//div[@id="houselistbody"]//div[@class="fanye"]').extract()

        if next_starturl is not None:
            next_url = self.Net_Url(next_starturl)
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, cookies=self.cookies)

    # 分解租房类型、厅、室、面积
    def font_mt_bold(self, data, item):
        if len(data):
            rex = "\|"
            rex_room_hall = r'\d'
            rex_area = r'(.*?)㎡'

            type_room_hall_area = re.split(rex, ''.join(data).strip())

            item['mode'] = type_room_hall_area[0]  # 租房类型
            room_hall = re.findall(rex_room_hall, type_room_hall_area[1])
            data_area = re.findall(rex_area, type_room_hall_area[2])[0].strip()

            if len(room_hall) == 2:
                item['room'] = int(room_hall[0].strip())  # 室
                item['hall'] = int(room_hall[1].strip())  # 厅
            else:
                item['room'] = 0
                item['hall'] = -1
            item['area'] = int(data_area)  # 房屋面积
            if len(type_room_hall_area) == 4:
                item['orientations'] = type_room_hall_area[3]  # 房屋朝向
            else:
                item['orientations'] = 'Nostr'
        else:
            for i in range(0, 4):
                data.append('Nostr')

    # 组合离地铁站距离
    def Subway(self, subway_distance, item):
        if len(subway_distance):
            subway = ''.join(subway_distance)
            subway_number = re.search(r'\d+', subway)
            item['subway'] = subway_number.group(0)
        else:
            item['subway'] = -1

    # 房屋信息
    def NoteF(self, note, item):
        if len(note) == 3:
            item['note_one'] = note[0]
            item['note_two'] = note[1]
            item['note_three'] = note[2]
        elif len(note) == 2:
            item['note_one'] = note[0]
            item['note_two'] = note[1]
            item['note_three'] = 'no'
        elif len(note) == 1:
            item['note_one'] = note[0]
            item['note_two'] = 'no'
            item['note_three'] = 'no'
        else:
            item['note_one'] = 'no'
            item['note_two'] = 'no'
            item['note_three'] = 'no'

    # 获取下一页
    def Net_Url(self, next_starturl):
        next_url = ''.join(next_starturl)
        rex = r'<a href="(.*?)">(.*?)</a>'
        urls = re.findall(rex, next_url)
        data = str()
        for url in urls:
            if '下一页' in url:
                data = url[0]
        return data
