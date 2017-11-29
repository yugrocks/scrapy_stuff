from scrapy.exporters import CsvItemExporter


class BlogscrapperPipeline(object):
    def process_item(self, item, spider):
        return item

class CsvPipeline(object):
    def __init__(self):
        self.file = open("posts.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class CsvPipeline2(object):
    def __init__(self):
        self.file = open("family_and_relationships.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
