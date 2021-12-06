import json

import scrapy
from scrapy import Request

from fans.items import FansItem


class YysdfanSpider(scrapy.Spider):
    name = 'yysdfan'
    allowed_domains = ['yyds.fans']
    start_urls = ['https://cmn.yyds.fans/api/posts']
    data = {
        "category_id": "-1", "skip": "0", "limit": "30", "keyword": ""
    }
    del_data = {
        "id": ""
    }
    header = {'Content-Type': 'application/json'}
    _exit = True

    def start_requests(self):
        print(f"请求了")
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, formdata=self.data, callback=self.parse)

    def parse(self, response):
        print(f"data", response.json())

        urls = 'https://cmn.yyds.fans/api/posts'
        # 翻页
        page_curr = 1
        while self._exit:
            if self._exit is True:
                print(f"第{page_curr}")
                page_curr += 30
                self.data['skip'] = page_curr
                print(f"_exit的值", self._exit)
                print(f"data", json.dumps(self.data))
                yield Request(url=urls, method='POST', body=json.dumps(self.data), headers=self.header,
                              callback=self.parse_json)
            else:
                break

    # 翻页的json
    def parse_json(self, response):
        _data = response.json()
        if _data['data'] is None:
            print(f"数据为null")
            self._exit = False  # 没数据不在翻页
            return self._exit
        for _node in _data['data']:
            item = FansItem()
            item['request_id'] = _node['id']
            item['title'] = _node['title']
            # _tags = [_node['tags'][tag] for tag in range(len(_node['tags']))
            #          if not len(_node['tags'][tag]) == 0]

            if not len(_node['tags']) == 0:
                # print(f"tags长度", len(_node['tags']))
                # print(f"tags", _node['tags'])
                # print(f"tags", _node['tags'][0]['id'])
                # print(f"tags", _node['tags'][0]['title'])
                # print(f"_node['tags']", _node['tags'])

                ind = len(_node['tags'])
                # print(f"tags", _node['tags'])
                # print(f"index", _node['tags'][ind - 1]['title'])

                # print(f"no", ind)
                # print(f"index", _node['tags'][0]['title'])
                _titles = ""
                _ids = []
                for i in _node['tags']:
                    _titles += i['title'] + ","
                    _ids.append(i['id'])
                    # print(f"循环tag_id", i['id'])
                _titles = _titles.split(',')
                item['tags'] = _ids
                item['tag_title'] = _titles
                item['del_url'] = "https://cmn.yyds.fans/api/post-info/"
                self.del_data['id'] = _node['id']
                yield Request(url=item['del_url'], method='POST', meta={'item': item}, body=json.dumps(self.del_data),
                              headers=self.header,
                              priority=10, dont_filter=True,
                              callback=self.parse_detail)
            else:
                print(f"tags为null")

    def parse_del(self, response):
        item = response.meta["item"]
        print(f"详情", response.json())
        yield item
