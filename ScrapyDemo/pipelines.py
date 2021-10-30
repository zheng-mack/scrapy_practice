# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import scrapy
import re
import pymysql


class FangPipeline(object):
    def process_item(self, item, spider):
        if spider.name=='fang':
            db = pymysql.connect("localhost", "xxx", "xxx", "zufang")
            cursor = db.cursor()
            sql = 'INSERT INTO zf(name,address,rent,mode,room,hall,area,orientations,subway,note_one,note_two,note_three) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (
            item['name'], item['address'], item['rent'], item['mode'], item['room'], item['hall'], item['area'],
            item['orientations'], item['subway'], item['note_one'], item['note_two'], item['note_three']))
            db.commit()
            db.close()



class MoviePipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'meiju':
            with open("my_meiju.txt", 'a', encoding='utf-8') as fp:
                fp.write(item['name'] + '\n')
                fp.close()
        elif spider.name == 'douban':
            with open('doubanwang.txt', 'a', encoding='utf-8') as fp:
                fp.write('电影名字:' + item['dianying'] + '\n')
                fp.write('电影简介:' + item['jianjies'] + '\n')
                fp.write('电影评价:' + item['pingjia'] + '\n')
                fp.write('电影评分:' + item['pingfen'] + '\n\n')
            fp.close()
        elif spider.name == 'TongCheng':
            with open('tongcheng.txt', 'a', encoding='utf-8')as fp:
                fp.write(item['chengs'] + '|' + item['zhiwei'] + ' ' + item['gsname'] + '\n')
                fp.write('月薪：' + item['gongzi'] + '\n')
                fp.write('要求：' + item['yaoqiu'] + '\n')
                fp.write('待遇：' + item['daiyu'] + '\n')

                fp.write('\n')
            fp.close()


class Tongcheng(object):
    def process_item(self, item, spider):
        if spider.name == 'Tongcheng_nanny':
            with open('tongcheng_nanny.txt', 'a', encoding='utf-8')as fp:
                fp.write(item['nanny'])
                fp.write(',')
        elif spider.name=='TongCheng_money':
            headers = ['区域', '待遇', '工资', '公司名称', '职位']
            f = open('tongcheng.csv', 'a', encoding='utf-8')
            csv_writer = csv.writer(f)
            # 3. 构建列表头
            csv_writer.writerow(headers)
            # 4. 写入csv文件内容
            csv_writer.writerow([item['chengs'],item['daiyu'],item['gongzi'],item['gsname'],item['zhiwei']])
            # 5. 关闭文件
            f.close()


class MyProjectPipeline(object):
    def __init__(self):
        # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        self.f = open("liepin.csv", "a", newline="", encoding='utf8')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        self.fieldnames = ['chengs', 'daiyu', 'gongzi', 'gsname', 'zhiwei', 'xueli', 'jingyan']
        # # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)  #
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()

    def process_item(self, item, spider):
        # 写入spider传过来的具体数值
        self.writer.writerow(item)
        # 写入完返回
        return item

    def close(self, spider):
        self.f.close()

