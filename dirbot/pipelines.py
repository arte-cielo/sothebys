import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

from twisted.enterprise import adbapi
from scrapy import log
from datetime import datetime

import hashlib
from hashlib import md5

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    #words_to_filter = ['politics', 'religion']
    words_to_filter = ['politics']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item


class MyImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
    	for image_url in item['image_urls']:
        	yield scrapy.http.Request(image_url)


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
	print "INITIALguid: %s" % (guid)

     ##   conn.execute("""SELECT EXISTS(
     ##       SELECT 1 FROM aste WHERE guid = %s
     ##   )""", (guid,))
     ##   ret_aste = conn.fetchone()[0]
        
	conn.execute("""SELECT EXISTS(
            SELECT 1 FROM aste2 WHERE guid = %s
        )""", (guid,))
        aste2 = conn.fetchone()[0]

	if aste2:
            #conn.execute("""
            #    UPDATE aste
            #    SET name=%s, asta=%s, date=%s, time=%s, location=%s, maxlot=%s, update_date=%s
            #    WHERE guid=%s
            #""", (item['name'], '2000', item['date'], item['time'], item['location'], '20', now))
            #spider.log("Item updated in db: %s %r" % (guid, item))
            conn.execute("""
                UPDATE aste2
                SET name=%s, asta=%s, date=%s, time=%s, location=%s, maxlot=%s, update_date=%s
                WHERE guid=%s
            """, (item['name'], '5000', item['date'], item['time'], item['location'], '20', now))
            spider.log("Item updated in db: %s %s %s %s %s %s %s %s" % (guid, item['name'][0], '5000', item['date'][0], item['time'], item['location'], '20', now))
        else:
            conn.execute("""
                INSERT INTO aste2 ( guid, name, asta, date, time, location, maxlot, update_date)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
            """, ( guid, item['name'], '9000', item['date'], item['time'], item['location'], '90', now))
            spider.log("Item stored in db: %s %s %s %s %s %s %s %s" % (guid, item['name'], '9000', item['date'], item['time'], item['location'], '90', now))
            
	#guid = self._get_guid(item)
        
	#conn.execute("""SELECT EXISTS(
        #    SELECT 1 FROM opere WHERE id = %s
        #)""", (id,))
        #ret = conn.fetchone()[0]

    ## 	print "ret_aste: %s" % (ret_aste)
	print "now: %s" % (now)
	print "guid: %s" % (guid)
	print "linkurl: %s" % (item['linkurl'])

     ##   if ret_aste:
     ##       #conn.execute("""
     ##       #    UPDATE aste
     ##       #    SET name=%s, asta=%s, date=%s, time=%s, location=%s, maxlot=%s, update_date=%s
     ##       #    WHERE guid=%s
     ##       #""", (item['name'], '2000', item['date'], item['time'], item['location'], '20', now))
     ##       #spider.log("Item updated in db: %s %r" % (guid, item))
     ##       conn.execute("""
     ##           UPDATE aste
     ##           SET name=%s, asta=%s, date=%s, time=%s, location=%s, maxlot=%s, update_date=%s
     ##           WHERE guid=%s
     ##       """, (item['name'][0], '5000', item['date'], item['time'], item['location'], '20', now))
     ##       spider.log("Item updated in db: %s %s %s %s %s %s %s %s" % (guid, item['name'][0], '5000', item['date'][0], item['time'], item['location'], '20', now))
     ##   else:
     ##       conn.execute("""
     ##           INSERT INTO aste ( guid, name, asta, date, time, location, maxlot, update_date)
     ##           VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
     ##       """, ( guid, item['name'][0], '1000', item['date'][0], item['time'], item['location'], '10', now))
     ##       spider.log("Item stored in db: %s %s %s %s %s %s %s %s" % (guid, item['name'][0], '10000', item['date'][0], item['time'], item['location'], '10', now))
            
     ##       conn.execute("""
     ##           INSERT INTO artisti ( guid, author, name, surname, born, death, update_date)
     ##           VALUES ( %s, %s, %s, %s, %s, %s, %s)
     ##       """, ( guid, item['author'], item['author'].split()[0], item['author'].split()[1], item['date'][0].split('-')[0], item['date'][0].split('-')[1], now))
     ##       spider.log("Item stored in db autori: %s %s %s %s %s %s %s" % (guid, item['author'], "", "", item['date'], "", now))
            
     ##       #conn.execute("""
     ##       #    INSERT INTO opere (asta_id, author, period, title, lot, description, image_urls, image_paths, update_date)
     ##       #    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
     ##       #""", (1000, item['author'], item['period'], item['title'], item['maxlot'], item['description'], item['image_urls'], item['image_paths'], now))
     ##       #spider.log("Item stored in db: %r" % (item))
	    
    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        #return md5(item['location']).hexdigest()
        #returmd5(item['location']).hexdigest()
        return hashlib.md5(item["name"]).hexdigest()
        #return hashlib.md5(item['linkurl']).hexdigest()
