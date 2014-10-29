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
	#print "INITIALguid: %s" % (guid)

     ##   conn.execute("""SELECT EXISTS(
     ##       SELECT 1 FROM aste WHERE guid = %s
     ##   )""", (guid,))
     ##   ret_aste = conn.fetchone()[0]

	## check the t.aste.guid for insert or update         
	conn.execute("""SELECT EXISTS(
            SELECT 1 FROM aste2 WHERE guid = %s
        )""", (guid,))
        aste2 = conn.fetchone()[0]
	
	## check the t.aste.guid for insert or update         
	conn.execute("""SELECT EXISTS(
            SELECT 1 FROM opere WHERE guid = %s
        )""", (guid,))
        opere = conn.fetchone()[0]
        opere = 11

	print "ITEMNAME: %s" % item['name']
	
	if opere:
	    try:
            	conn.execute("""
                    UPDATE opere
                    SET name=%s, description=%s
                    WHERE guid=%s
            	""", (item['name'], item['descriptionr'], guid))
            	spider.log("ITEM ASTE UPDATE in db: %s %s %s" % (guid, item['name'], item['description']))
		
	    	print "UPDATE guid: %s" % (guid)
	    	print "UPDATE maxlot: %s" % (item['maxlot'])
	    	print "UPDATE sales_number: %s" % (item['sales_number'])
	    except :
		print 'UPDATE ASTE2 ERROR'
			
        else:
            conn.execute("""
                INSERT INTO opere ( guid, name, title, description, estimate, lot_sold, valuta, image_urls, image_path, images, url, update_date)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ( guid, item['name'], '', '', '', '', '', '', '', '', '', now))
            spider.log("ITEM STORED in db: %s %r" % (guid, item))
			
	
	if aste2:
	    try:
            	conn.execute("""
                    UPDATE aste2
                    SET maxlot=%s, sales_number=%s
                    WHERE guid=%s
            	""", (item['maxlot'], item['sales_number'], guid))
            	spider.log("ITEM ASTE UPDATE in db: %s %s %s" % (guid, item['maxlot'], item['sales_number']))
		
	    	#print "UPDATE guid: %s" % (guid)
	    	#print "UPDATE maxlot: %s" % (item['maxlot'])
	    	#print "UPDATE sales_number: %s" % (item['sales_number'])
	    except :
		print 'UPDATE ASTE2 ERROR'
			
        else:
            conn.execute("""
                INSERT INTO aste2 ( guid, name, asta, date, linkurl, location, maxlot, update_date)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
            """, ( guid, item['name'], item['asta'], item['date'], item['linkurl'], item['location'], '', now))
            spider.log("ITEM STORED in db: %s %s %s %s %s %s %s %s" % (guid, item['name'], item['asta'], item['date'], item['linkurl'], item['location'], '', now))
            
    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        #return md5(item['location']).hexdigest()
        #returmd5(item['location']).hexdigest()
        epure = item["name"].encode('ascii','ignore')
	print epure
        #return hashlib.md5(item["name"]).encode('acii','ignore').hexdigest()
        return hashlib.md5(epure).hexdigest()
