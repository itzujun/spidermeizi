# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request


class SpidermeiziPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        headers = {
            "Referer": "https://www.mzitu.com/"
        }
        for url in item["imgurls"]:
            yield Request(url, headers=headers, meta={"name": item["name"]})

    def item_completed(self, results, item, info):
        # print("result ====> : ", results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        print("下载完成: ", image_paths)
        return item

    def file_path(self, request, response=None, info=None):
        name = request.meta['name']
        image_guid = request.url.split('/')[-1]
        # print("image_guid:", image_guid, "  name:", name)
        filenames = "zujun/%s/%s" % (name, image_guid)
        return filenames
