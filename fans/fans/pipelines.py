# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from fans.Sqlhelper.hepler import DBHelper


class FansPipeline:
    def process_item(self, item, spider):
        _mysql = DBHelper()
        _exit_sql = 'SELECT request_id FROM Movies m WHERE request_id =%s'
        _exit_age = (item['request_id'])

        _insert_sql = "INSERT INTO `Movies`" \
                      "(Title, Tags, request_id, del_url, next_url, subtitle, cover, created_at, Links,Context)" \
                      " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        _insert_age = (item['title'], 1, item['request_id'],
                       item['insert_del'], item['subtitle'], item['cover'], "null", "null", 'null', 'null'
                       )
        _result = _mysql.insert(_insert_sql, _insert_age)
        print(f"_result", _result)
        return item
