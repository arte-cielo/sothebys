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

import string
import random
import psycopg2


mailer = MailSender(
    smtphost="mx.artecielo.com",
    mailfrom="scrapy@localhost",
    smtpuser="info@artecielo.com",
    smtppass="Blacking1",
)


class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    # words_to_filter = ['politics', 'religion']
    words_to_filter = ["politics"]

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item["description"]).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield scrapy.http.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        #item["image_paths"] = image_paths
        item["downloadhref"] = image_paths
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
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset="utf8",
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbargs)
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
        now = datetime.utcnow().replace(microsecond=0).isoformat(" ")

        # check the t.aste.guid for insert or update
        conn.execute(
            """SELECT EXISTS(
            SELECT 1 FROM aste2 WHERE guid = %s
        )""",
            (guid,),
        )
        aste2 = conn.fetchone()[0]

        # check if exists a quarantena auction with
        # status 'Q' and report at info@
        conn.execute(
            """SELECT *
            FROM aste2 WHERE status = "Q"
        """
        )
        qstatus = conn.fetchall()

        # print 'AUCTIONS Q STATUS: %s' % qstatus
        # if qstatus:
        #    mailer.send(to=["info@artecielo.com"], subject="Attenzione! Quarentena aste:"+qstatus[2], body="Hai aste in quarantena:\n Asta:"+qstatus[1]+'\n'+"Data:"+qstatus[3])

        ##opere = conn.fetchone()[0]
        print "AFTERITEMNAME: %s" % item["name"]
        print "AFTERITEMSTATUS: %s" % item["status"]
        print "AFTERGUID: %s" % guid
        print "AFTERMAXLOT: %s" % item["maxlot"]
        print "AFTERSALES: %s" % item["sales_number"]
        print "AFTERSTATUS: %s" % item["status"]
        print "AFTERDOWNLODHREF: %s" % item["downloadhref"]
        print "AFTERSALE_TOTAL: %s" % item["sale_total"]
        # print "AFTERASTA: %s" % item['asta']
        print "AFTERLINKURL: %s" % item["linkurl"]
        # print "LOCATION: %s" % item['location']
        print "AFTERGUID: %s" % guid

        # AND status <> "CD" AND sale_total = 0 OR sale_total IS NULL
        if aste2:
            try:
                conn.execute(
                    """
                UPDATE aste2
                SET maxlot=%s, name=%s, linkurl=%s, sales_number=%s, status=%s, date=%s, category=%s, overview=%s, downloadhref=%s, sale_total=%s, update_date=%s, layout=%s
                WHERE guid=%s
		        AND status <> "CD"
            	""",
                    (
                        item["maxlot"],
                        item["name"],
                        item["linkurl"],
                        item["sales_number"],
                        item["status"],
                        item["date"],
                        item["category"],
                        item["overview"],
                        item["downloadhref"],
                        item["sale_total"],
                        now,
                        "layout",
                        guid,
                    ),
                )
                spider.log("ITEM ASTE UPDATE in db: %s %r" % (guid, item))

                mailer.send(
                    to=["info@artecielo.com"],
                    subject="Completo Asta inserita:" + item["sales_number"],
                    body="Ho aggiornato i seguenti dati:\n Asta:"
                    + item["sales_number"]
                    + "\n"
                    + "Lotti:"
                    + str(
                        item["maxlot"] + "\n"
                        "Status:"
                        + item["status"]
                        + "\n"
                        + "DownloadHref: http://www.sothebys.com"
                        + item["downloadhref"]
                    ),
                )

            except BaseException:
                print "ERROR: UPDATE ASTE2 "
                print "ERROR: UPDATE guid: %s" % (guid)
                print "ERROR: UPDATE maxlot: %s" % (item["maxlot"])
                print "ERROR: UPDATE sales_number: %s" % (item["sales_number"])
                print "ERROR: UPDATE status: %s" % (item["status"])
                print "ERROR: UPDATE date: %s" % (item["date"])
                print "ERROR: UPDATE downloadhref: %s" % (item["downloadhref"])
                print "ERROR: UPDATE sale_total: %s" % (item["sale_total"])
                print "ERROR: UPDATE name: %s" % (item["name"])

        # elif qstatus:
        # 	for cc in qstatus:
        #    	    mailer.send(to=["info@artecielo.com"], subject="Attenzione! Quarentena aste:"+cc[2], body="Hai aste in quarantena:\n Asta:"+cc[1]+'\n'+"Data:"+cc[3])
        else:
            # very important here: some fields are update in UPDATE ASTE
            # (second step): they are item[downloadhref] and item[maxlot]
            conn.execute(
                """
                INSERT INTO aste2 ( guid, name, asta, date, datafine, category, overview, linkurl, downloadhref, location, maxlot, status, sales_number, sale_total, layout, update_date, calendario_id, caseasta_id)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    guid,
                    item["name"],
                    item["asta"],
                    item["date"],
                    item["date"],
                    item["category"],
                    "",
                    item["downloadhref"],
                    item["downloadhref"],
                    item["location"],
                    item["maxlot"],
                    item["status"],
                    item["sales_number"],
                    item["sale_total"],
                    "layout",
                    now,
                    999,
                    1,
                ),
            )
            spider.log("ITEM STORED in t.ASTE2: %s %r" % (guid, item))
            mailer.send(
                to=["info@artecielo.com"],
                subject="Nuova Asta inserita:" + item["asta"],
                body="Ho inserito alcune nuove aste:\n Asta:"
                + item["name"]
                + "\n"
                + "Lotti:"
                + str(item["maxlot"]),
            )

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        # return md5(item['location']).hexdigest()
        # returmd5(item['location']).hexdigest()
        # epure = item["name"].encode('ascii','ignore')+(''.join(random.choice(string.ascii_uppercase) for i in range(12)))
        epure = str(item["linkurl"])
        # epure = str(item["name"])
        print "EPURE: %s" % epure
        # return hashlib.md5(item["name"]).encode('acii','ignore').hexdigest()
        return hashlib.md5(epure).hexdigest()

class DirBotPostresPipeline(object):

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        # return md5(item['location']).hexdigest()
        # returmd5(item['location']).hexdigest()
        # epure = item["name"].encode('ascii','ignore')+(''.join(random.choice(string.ascii_uppercase) for i in range(12)))
        epure = str(item["linkurl"])
        # epure = str(item["name"])
        print "EPURE: %s" % epure
        # return hashlib.md5(item["name"]).encode('acii','ignore').hexdigest()
        return hashlib.md5(epure).hexdigest()

    def open_spider(self, spider):
        hostname = '192.168.1.5'
        username = 'postgres'
        password = '***' # your password
        database = 'artecielo'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(" ")
        # check the t.aste.guid for insert or update
        exists_guid ='''SELECT EXISTS (SELECT 1 FROM aste2 WHERE guid = %s)'''
        self.cur.execute(exists_guid, (guid,))
        #self.cur.execute(
        #    """SELECT EXISTS(
        #    SELECT 1 FROM aste2 WHERE guid = %s
        #)""",
        #    (guid,))

        aste2 = self.cur.fetchone()[0]
        print('ASTE2 %s', aste2)

        # check if exists a quarantena auction with
        # status 'Q' and report at info@
        #status = '''Q'''
        #exists_status ='''SELECT FROM aste2 WHERE status = %s)'''
        #self.cur.execute(exists_status, (status,))
        self.cur.execute(
            """SELECT *
            FROM aste2 WHERE status = %s
            """,
            ("Q"),
        )
        qstatus = self.cur.fetchall()

        ##opere = conn.fetchone()[0]
        print "AFTERITEMNAME: %s" % item["name"]
        print "AFTERITEMSTATUS: %s" % item["status"]
        print "AFTERGUID: %s" % guid
        print "AFTERMAXLOT: %s" % item["maxlot"]
        #print "AFTERSALES: %s" % item["sales_number"]
        print "AFTERSTATUS: %s" % item["status"]
        print "AFTERDOWNLODHREF: %s" % item["downloadhref"]
        print "AFTERSALE_TOTAL: %s" % item["sale_total"]
        # print "AFTERASTA: %s" % item['asta']
        print "AFTERLINKURL: %s" % item["linkurl"]
        # print "LOCATION: %s" % item['location']
        print "AFTERGUID: %s" % guid

        # AND status <> "CD" AND sale_total = 0 OR sale_total IS NULL
        if aste2:
            try:
                self.cur.execute(
                    """
                UPDATE aste2
                SET maxlot=%s, name=%s, linkurl=%s, sales_number=%s, status=%s, date=%s, category=%s, overview=%s, downloadhref=%s, sale_total=%s, update_date=%s, layout=%s
                WHERE guid=%s
		        AND status <> "CD"
            	""",
                    (
                        item["maxlot"],
                        item["name"],
                        item["linkurl"],
                        item["sales_number"],
                        item["status"],
                        item["date"],
                        item["category"],
                        item["overview"],
                        item["downloadhref"],
                        item["sale_total"],
                        now,
                        "layout",
                        guid,
                    ),
                )
                spider.log("ITEM ASTE UPDATE in db: %s %r" % (guid, item))

                mailer.send(
                    to=["info@artecielo.com"],
                    subject="Completo Asta inserita:" + item["sales_number"],
                    body="Ho aggiornato i seguenti dati:\n Asta:"
                    + item["sales_number"]
                    + "\n"
                    + "Lotti:"
                    + str(
                        item["maxlot"] + "\n"
                        "Status:"
                        + item["status"]
                        + "\n"
                        + "DownloadHref: http://www.sothebys.com"
                        + item["downloadhref"]
                    ),
                )

            except BaseException:
                print "ERROR: UPDATE ASTE2 "
                print "ERROR: UPDATE guid: %s" % (guid)
                print "ERROR: UPDATE maxlot: %s" % (item["maxlot"])
                print "ERROR: UPDATE sales_number: %s" % (item["sales_number"])
                print "ERROR: UPDATE status: %s" % (item["status"])
                print "ERROR: UPDATE date: %s" % (item["date"])
                print "ERROR: UPDATE downloadhref: %s" % (item["downloadhref"])
                print "ERROR: UPDATE sale_total: %s" % (item["sale_total"])
                print "ERROR: UPDATE name: %s" % (item["name"])

        # elif qstatus:
        # 	for cc in qstatus:
        #    	    mailer.send(to=["info@artecielo.com"], subject="Attenzione! Quarentena aste:"+cc[2], body="Hai aste in quarantena:\n Asta:"+cc[1]+'\n'+"Data:"+cc[3])
        else:

            self.cur.execute("insert into aste2( guid, name, asta, date, datafine, category, overview, linkurl, downloadhref," \
                            "location,  maxlot, status, sales_number, sale_total, layout, update_date, calendario_id, caseasta_id)" \
                            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                                (
                                    guid,
                                    item['name'],
                                    item['asta'],
                                    item['date'],
                                    item['date'],
                                    item['category'],
                                    "",
                                    item["downloadhref"],
                                    item["downloadhref"],
                                    item["location"],
                                    item["maxlot"],
                                    item["status"],
                                    item["sales_number"],
                                    item["sale_total"],
                                    "layout",
                                    now,
                                    999,
                                    1,
                                )
                            )
        self.connection.commit()
        return item
