import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

from twisted.enterprise import adbapi
from scrapy import log
from datetime import datetime

import hashlib
from hashlib import md5

from scrapy import *
from scrapy.mail import MailSender

mailer = MailSender(smtphost="mx.artecielo.com",mailfrom="scrapy@localhost",smtpuser="info@artecielo.com",smtppass="Blacking1")

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
	
	## check the t.aste.guid for insert or update         
	conn.execute("""SELECT EXISTS(
            SELECT 1 FROM aste2 WHERE guid = %s
        )""", (guid,))
        aste2 = conn.fetchone()[0]
	
	## check if exists a quarantena auction with 
        ## status 'Q' and report at info@ 
	conn.execute("""SELECT *
            FROM aste2 WHERE status = "Q"
        """ )
        qstatus = conn.fetchall()

	print qstatus	
	#if qstatus:
	#    mailer.send(to=["info@artecielo.com"], subject="Attenzione! Quarentena aste:"+qstatus[2], body="Hai aste in quarantena:\n Asta:"+qstatus[1]+'\n'+"Data:"+qstatus[3])
			 
	#print "BEFOREITEMNAME: %s" % item['name']
	#print "BEFOREQSTATAUS: %s" % str(qstatus[8])
	##if qstatus:
	##    print "*********QSTATUS*********"+str(aste2)
	##    if str(qstatus[8]) == "Q":
	##        print qstatus
	##	print "QSTATUSITEMNAME: %s" % item['name']
	##	print "QSTATAUSTATUS: %s" % str(qstatus[8])
	##	print "QSTATUSSALE_TOTAL: %s" % item['sale_total']
	##	guid = str(qstatus[0])
	##	item['status'] = "C"
	##	if item['sale_total'] is None:
	##	    item['sale_total'] = 0
	##	aste2 = 1
	
	## check the t.aste.guid for insert or update         
	##conn.execute("""SELECT EXISTS(
        ##    SELECT 1 FROM opere WHERE guid = %s
        ##)""", (guid,))
        ##opere = conn.fetchone()[0]
	print "****************************"+str(aste2)
	print "AFTERITEMNAME: %s" % item['name']
	print "AFTERITEMSTATUS: %s" % item['status']
	print "AFTERGUID: %s" % guid 
	print "AFTERMAXLOT: %s" % item['maxlot'] 
	print "AFTERSALES: %s" % item['sales_number']
	print "AFTERSTATUS: %s" % item['status']
	print "AFTERDOWNLODHREF: %s" % item['downloadhref']
	print "AFTERSALE_TOTAL: %s" % item['sale_total']
	#print "AFTERASTA: %s" % item['asta']
	
	if aste2:
	    try:
            	conn.execute("""
                    UPDATE aste2
                    SET maxlot=%s, sales_number=%s, status=%s, downloadhref=%s, sale_total=%s, update_date=%s, layout=%s
                    WHERE guid=%s
		    AND status <> "CD"
            	""", (item['maxlot'], item['sales_number'], item['status'], item['downloadhref'], item['sale_total'], now, 'layout', guid))
            	spider.log("ITEM ASTE UPDATE in db: %s %r" % (guid, item))
	    
	        mailer.send(to=["info@artecielo.com"], subject="Completo Asta inserita:"+item['sales_number'], body="Ho aggiornato i seguenti dati:\n Asta:"+item['sales_number']+'\n'+"Lotti:"+str(item['maxlot']+"\n""Status:"+item['status']+"\n"+"DownloadHref: http://www.sothebys.com"+item['downloadhref']))
		
	    	#print "UPDATE guid: %s" % (guid)
	    	#print "UPDATE maxlot: %s" % (item['maxlot'])
	    	#print "UPDATE sales_number: %s" % (item['sales_number'])
	    except :
		print 'UPDATE ASTE2 ERROR'
	    	print "UPDATE ERROR guid: %s" % (guid)
	    	print "UPDATE ERROR maxlot: %s" % (item['maxlot'])
	    	print "UPDATE ERROR sales_number: %s" % (item['sales_number'])
	    	print "UPDATE ERROR sale_total: %s" % (item['sale_total'])
	    	print "UPDATE ERROR status: %s" % (item['status'])

	#elif qstatus:
	#	for cc in qstatus:
	#    	    mailer.send(to=["info@artecielo.com"], subject="Attenzione! Quarentena aste:"+cc[2], body="Hai aste in quarantena:\n Asta:"+cc[1]+'\n'+"Data:"+cc[3])
        else:
	    ##very important here: some fields are update in UPDATE ASTE (second step): they are item[downloadhref] and item[maxlot] 
            conn.execute("""
                INSERT INTO aste2 ( guid, name, asta, date, linkurl, downloadhref, location, maxlot, status, sales_number, layout, update_date, calendario_id, caseasta_id)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ( guid, item['name'], item['asta'], item['date'], item['linkurl'], 'downloadhref', item['location'], 'maxlot', item['status'], 'sales_number', 'layout', now, 999, 1))
            spider.log("ITEM STORED in t.ASTE: %s %r" % (guid, item))
	    mailer.send(to=["info@artecielo.com"], subject="Nuova Asta inserita:"+item['asta'], body="Ho inserito alcune nuove aste:\n Asta:"+item['name']+'\n'+"Lotti:"+str(item['maxlot']))
            
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
        #epure = str(item["name"])
	print 'EPURE: %s' % epure
        #return hashlib.md5(item["name"]).encode('acii','ignore').hexdigest()
        return hashlib.md5(epure).hexdigest()
