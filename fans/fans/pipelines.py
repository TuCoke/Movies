# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class FansPipeline:
    def process_item(self, item, spider):
        _exit_sql = 'SELECT request_id FROM Movies m WHERE request_id =%s'
        _exit_age = (item['request_id'])

        _insert_sql = "INSERT INTO `Movies`" \
                      "(Title, Tags, request_id, del_url, next_url, subtitle, cover, created_at, Links)" \
                      " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        return item
