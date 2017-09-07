# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.exporter import CsvItemExporter
import datetime, os, codecs
class PaipaidaiPipeline(object):
    # 调用scrapy 提供的csv exporter 导出csv文件
    def __init__(self):
        data_file = "%s.csv" % (datetime.datetime.now().strftime("%Y-%m-%d"))
        if os.path.exists(data_file):
           self.file = open(data_file,"ab+")
           self.exporter = CsvItemExporter(self.file,include_headers_line=True,encoding="gbk")
        else:
            self.file = open(data_file, "wb+")
            self.exporter = CsvItemExporter(self.file, include_headers_line=True, encoding="gbk")

        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()


class PaipaidaiItemsPipeline(object):
    def __init__(self,settings):
        TODAY_ITEM_FILES = settings['TODAY_ITEM_FILES']
        self.f = codecs.open(TODAY_ITEM_FILES,"w+",encoding="utf-8")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)


    def process_item(self, item, spider):
        dict_item = dict(item)
        value = dict_item['itemid']
        self.f.write("%s\n" % value)
        print (value,":done")
        return item


    def close_spider(self, spider):
        self.f.close()