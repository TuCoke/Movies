import json
import time

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
    header = {'Content-Type': 'application/json',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41',
              'origin': 'https://yyds.fans'
              }

    def start_requests(self):
        print(f"请求了")
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, formdata=self.data, callback=self.parse)

    def parse(self, response):
        data = response.json()
        print(f"data", response.json())
        print(f"data状态", data['status_code'])
        urls = 'https://cmn.yyds.fans/api/posts'
        # 翻页
        # page_curr = 1
        # print(f"第{page_curr}")
        # page_curr += 1
        # self.data['skip'] = page_curr
        # print(f"data", json.dumps(self.data))
        page = 2
        while True:
            page += 1
            print('*' * 50)
            # print("正在爬取第 %s 页" % page)
            if page < 999:
                yield Request(url=urls, method='POST', body=json.dumps(self.data), headers=self.header,
                              callback=self.parse_json)
            else:
                # print("结束 %s 页" % page)
                break

    # 翻页的json
    def parse_json(self, response):
        _data = response.json()
        print(f"_data", _data['status_code'])
        if _data['status_code'] == 429:
            print(f"数据为null")
        else:
            for _node in _data['data']:
                item = FansItem()
                item['request_id'] = _node['id']
                item['title'] = _node['title']
                item['cover'] = _node['cover']
                item['subtitle'] = _node['subtitle']
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
                    # print("https://cmn.yyds.fans/api/post-info/%s" % _node['id'])
                    item['insert_del'] = "https://cmn.yyds.fans/api/post-info/%s" % _node['id']
                    self.del_data['id'] = _node['id']
                    yield Request(url=item['del_url'], method='POST', meta={'item': item},
                                  body=json.dumps(self.del_data),
                                  headers=self.header,
                                  callback=self.parse_detail)
                else:
                    print(f"tags为null")

    def parse_detail(self, response):
        item = response.meta["item"]
        print(f"详情", response.json())
        _data = response.json()
        # item['content'] = _data['data']['content']
        _links = _data['data']['links']
        yield item
