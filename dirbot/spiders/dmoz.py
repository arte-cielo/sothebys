from scrapy.spider import Spider, BaseSpider
from scrapy.selector import Selector

from dirbot.items import Website, AsteWebsite

from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy import *
from scrapy.mail import MailSender

from urlparse import urlparse

mailer = MailSender()
# mailer.send(to=["marco.giardina@gmail.com"], subject="Some subject", body="Some body", cc=["info@mammagatto.org"])


class DmozSpider(BaseSpider):
    name = "sothebys"

    def __init__(self, facility=None, *args, **kwargs):
        super(DmozSpider, self).__init__(*args, **kwargs)
        # self.start_urls = ['http://www.example.com/categories/%s' % category]

        # introduce facility costructor
        # @ facility is:
        # @ - more start_urls = 1
        # @ - custom category = 2
        # @ - single asta = 3

        # @ for example:
        # @ scrapy crawl sothebys -a facility=1 [ -a domain=system]

    allowed_domains = ["sothebys.com"]
    start_urls = [
        "https://www.sothebys.com/en/buy/auction/2021/master-paintings-sculpture-part-i?locale=en",
        #"https://www.sothebys.com/en/buy/auction/2021/quality-in-detail-the-juli-and-andrew-wieg-collection?locale=en",
        #"https://www.sothebys.com/en/buy/auction/2019/old-master-drawings?locale=en",
        # "http://www.sothebys.com/en/auctions/2017/victorian-pre-raphaelite-british-impressionist-art-l17132.html",
        # "http://www.sothebys.com/it/auctions/2016/boundless-contemporary-art-hk0703.html",
        # "http://www.sothebys.com/en/auctions/2016/russian-pictures-l16112.html",
        # "http://www.sothebys.com/en/auctions/2016/art-impressionniste-et-moderne-pf1606.html",
        # "http://www.sothebys.com/en/auctions/2015/impressionist-modern-art-n09509.html#&page=all&sort=lotSortNum-asc&range=0|100&viewMode=list",
        # "http://www.sothebys.com/en/auctions/2016/master-paintings-n09515.html",
        # "http://www.sothebys.com/en/auctions/2016/arte-moderna-contemporanea-mi0329.html",
        # "http://www.sothebys.com/en/auctions/2016/19th-century-europzean-paintings-l16101.html",
        # "http://www.sothebys.com/en/auctions/2016/19th-20th-century-sculpture-l16230.html",
        # "http://www.sothebys.com/en/auctions/2015/latin-america-modern-contemporary-art-n09508.html",
        # "http://www.sothebys.com/en/auctions/2016/american-art-n09503.html",
        # "http://www.sothebys.com/en/auctions/2016/19th-century-european-art-n09499.html",
        # "http://www.sothebys.com/en/auctions/2016/impressionist-modern-art-day-sale-n09498.html",
        # "http://www.sothebys.com/en/auctions/2016/impressionist-modern-art-evening-sale-n09497.html",
        # "http://www.sothebys.com/en/auctions/2016/chinese-art-caramoor-center-music-arts-n09476.html",
        # "http://www.sothebys.com/en/auctions/2016/contemporary-curated-n09473.html",
        # "http://www.sothebys.com/en/auctions/2015/important-chinese-art-n09477.html",
        # "http://www.sothebys.com/en/auctions/2015/modern-contemporary-south-asian-art-n09479.html",
        # "http://www.sothebys.com/en/auctions/2016/watches-l16053.html",
        # "http://www.sothebys.com/en/auctions/2016/now-pf1650.html",
        # "http://www.sothebys.com/en/auctions/2016/surrealist-art-evening-sale-l16003.html",
        # "http://www.sothebys.com/en/auctions/2016/impressionist-modern-art-evening-sale-l16002.html",
        # "http://www.sothebys.com/en/auctions/2016/contemporary-art-day-l16021.html",
        # "http://www.sothebys.com/en/auctions/2016/contemporary-art-evening-auction-l16020.html",
        # "http://www.sothebys.com/en/auctions/2016/picasso-in-private-collection-marina-picasso-l16005.html",
        # "http://www.sothebys.com/en/auctions/2016/impressionist-modern-art-day-sale-l16004.html",
        # "http://www.sothebys.com/en/auctions/2015/master-paintings-19th-century-european-art-n09459.html",
        # "http://www.sothebys.com/en/auctions/2016/important-americana-n09456.html",
        # "http://www.sothebys.com/en/auctions/2016/american-folk-art-collection-of-stephen-petra-levin-part-i-n09424.html",
        # "http://www.sothebys.com/en/auctions/2016/of-royal-and-noble-descent-l16306.html",
        # "http://www.sothebys.com/en/auctions/2016/important-americana-n09456.html",
        # "http://www.sothebys.com/en/auctions/2015/20th-century-art-l15103.html",
        # "http://www.sothebys.com/en/auctions/2015/library-english-bibliophile-part-five-l15416.html",
        # "http://www.sothebys.com/en/auctions/2015/american-art-collection-a-alfred-taubman-n09432.html",
        # "http://www.sothebys.com/en/auctions/2015/design-20-siecle-pf1514.html",
        # "http://www.sothebys.com/en/auctions/2015/american-art-collection-a-alfred-taubman-n09432.html",
        # "http://www.sothebys.com/en/auctions/2015/russian-pictures-l15115.html",
        # "http://www.sothebys.com/en/auctions/2015/fine-timepieces-hk0600.html",
        # "http://www.sothebys.com/en/auctions/2015/arte-moderna-contemporanea-mi0327.html",
        # "http://www.sothebys.com/en/auctions/2015/latin-america-modern-art-n09428.html",
        # "http://www.sothebys.com/en/auctions/2015/american-art-n09425.html",
        # "http://www.sothebys.com/en/auctions/2015/modern-post-war-british-art-l15143.html",
        # "http://www.sothebys.com/en/auctions/2015/travel-atlases-maps-natural-history-l15405.html#&page=all&sort=lotSortNum-asc&range=0|100&viewMode=list",
        # "http://www.sothebys.com/en/auctions/2015/photographies-pf1520.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-art-evening-auction-n09420.html",
        # "http://www.sothebys.com/en/auctions/2015/american-art-collection-a-alfred-taubman-n09432.html",
        # "http://www.sothebys.com/en/auctions/2015/scottish-art-l15135.html",
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-n09416.html",
        # "http://www.sothebys.com/en/auctions/2015/impressionist-modern-art-evening-sale-n09415.html",
        # "http://www.sothebys.com/en/auctions/2015/modern-contemporary-art-collection-a-alfred-taubman-n09431.html",
        # "http://www.sothebys.com/en/auctions/2015/masterworks-collection-a-alfred-taubman-n09430.html",
        # "http://www.sothebys.com/en/auctions/2015/19th-century-european-art-n09417.html",
        # "http://www.sothebys.com/en/auctions/2015/collections-l15305.html",
        # "http://www.sothebys.com/en/auctions/2015/old-master-paintings-l15035.html",
        # "http://www.sothebys.com/en/auctions/2015/the-italian-sale-l15624.html",
        # "http://www.sothebys.com/en/auctions/2015/irish-art-l15134.html",
        # "http://www.sothebys.com/en/auctions/2015/vajrayana-voyage-to-the-tantra-hk0595.html",
        # "http://www.sothebys.com/en/auctions/2015/imperial-consort-hk0596.html",
        # "http://www.sothebys.com/en/auctions/2015/imperial-interiors-hk0594.html",
        # "http://www.sothebys.com/en/auctions/2015/important-chinese-art-hk0591.html",
        # "http://www.sothebys.com/en/auctions/2015/full-circle-yoshihara-jiro-collection-hk0653.html",
        # "http://www.sothebys.com/en/auctions/2015/modern-contemporary-southeast-asian-art-hk0584.html",
        # "http://www.sothebys.com/en/auctions/2015/classical-chinese-paintings-hk0588.html",
        # "http://www.sothebys.com/en/auctions/2015/modern-contemporary-asian-art-evening-sale-hk0581.html",
        # "http://www.sothebys.com/en/auctions/2015/american-paintings-drawings-sculpture-n09404.html",
        # "http://www.sothebys.com/en/auctions/2014/prints-and-multiples-l15161.html",
        # "http://www.sothebys.com/en/auctions/2015/images-of-enlightenment-n09395.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-curated-n09403.html",
        # "http://www.sothebys.com/en/auctions/2015/collection-histoire-famille-france-pf1531.html",
        # "http://www.sothebys.com/en/auctions/2015/watches-l15053.html",
        # "http://www.sothebys.com/en/auctions/2015/saturday-at-sothebys-asian-art-n09437.html",
        # "http://www.sothebys.com/en/auctions/2015/fine-classical-chinese-paintings-calligraphy-n09394.html",
        # "http://www.sothebys.com/en/auctions/2015/important-chinese-art-n09393.html",
        # "http://www.sothebys.com/en/auctions/2015/monochrome-n09396.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-art-evening-auction-l15022.html",
        # "http://www.sothebys.com/en/auctions/2015/now-pf1524.html",
        # "http://www.sothebys.com/en/auctions/2015/watches-n09368.html",
        # "http://www.sothebys.com/en/auctions/2015/finest-and-rarest-wines-n09349.html",
        # "http://www.sothebys.com/en/auctions/2015/finest-rarest-wines-l15706.html",
        # "http://www.sothebys.com/en/auctions/2015/tableaux-dessins-anciens-19-siecle-pf1509.html",
        # "http://www.sothebys.com/en/auctions/2015/books-manuscripts-n09359.html",
        # "http://www.sothebys.com/en/auctions/2015/arts-afrique-oceanie-pf1508.html",
        # "http://www.sothebys.com/en/auctions/2015/impressionist-modern-art-evening-sale-l15006.html",
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-l15007.html",
        # "http://www.sothebys.com/en/auctions/2015/livres-manuscrits-pf1503.html",
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-l15007.html",
        # "http://www.sothebys.com/en/auctions/2015/livres-manuscrits-pf1503.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-curated-n09366.html",
        # "http://www.sothebys.com/en/auctions/2015/fine-jewels-l15051.html",
        # "http://www.sothebys.com/en/auctions/2015/boundless-contemporary-art-hk0580.html",
        # "http://www.sothebys.com/en/auctions/2014/livres-manuscrits-pf1413.html",
        # "http://www.sothebys.com/en/auctions/2014/important-20th-c-design-n09238.html",
        # "http://www.sothebys.com/en/auctions/2014/tiffany-n09242.html",
        # "http://www.sothebys.com/en/auctions/2014/daughter-history-mary-soames-legacy-churchill-l14316.html",
        # "http://www.sothebys.com/en/auctions/2014/a-table-pf1460.html",
        # "http://www.sothebys.com/en/auctions/2014/jon-stryker-collection-20-c-design-n09244.html",
        # "http://www.sothebys.com/en/auctions/2014/fine-jewels-l14052.html",
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-n09206.html",
        # "http://www.sothebys.com/en/auctions/2014/antiquities-n09236.html",
        # "http://www.sothebys.com/en/auctions/2014/finest-and-rarest-wines-hk0537.html",
        # "http://www.sothebys.com/en/auctions/2014/175-masterworks-n09275.html",
        # "http://www.sothebys.com/en/auctions/2014/masterworks-n09209.html",
        # "http://www.sothebys.com/en/auctions/2014/19th-century-sculpture-l14232.html",
        # "http://www.sothebys.com/en/auctions/2014/arts-asie-pf1417.html",
        # "http://www.sothebys.com/en/auctions/2014/alexis-bonew-congo-pf1448.html",
        # "http://www.sothebys.com/en/auctions/2014/watches-n09235.html",
        # "http://www.sothebys.com/en/auctions/2014/arts-afrique-oceanie-pf1418.html",
        # "http://www.sothebys.com/en/auctions/2014/19th-century-european-paintings-l14102.html",
        # "http://www.sothebys.com/en/auctions/2014/british-irish-art-l14133.html",
        # "http://www.sothebys.com/en/auctions/2014/finest-rarest-wines-l14712.html",
        # "http://www.sothebys.com/en/auctions/2014/magnificent-jewels-n09234.html",
        # "http://www.sothebys.com/en/auctions/2014/english-literature-history-childrens-books-illustrations-l14408.html",
        # "http://www.sothebys.com/en/auctions/2014/finest-and-rarest-wines-n09241.html",
        # "http://www.sothebys.com/en/auctions/2014/white-truffle-n09231.html",
        # "http://www.sothebys.com/en/auctions/2014/israeli-art-n09240.html",
        # "http://www.sothebys.com/en/auctions/2014/art-impressionniste-moderne-pf1416.html",
        # "http://www.sothebys.com/en/auctions/2014/important-judaica-n09239.html",
        # "http://www.sothebys.com/en/auctions/2014/old-master-british-paintings-day-l14037.html",
        # "http://www.sothebys.com/en/auctions/2014/old-master-british-paintings-evening-l14036.html",
        # "http://www.sothebys.com/en/auctions/2014/art-contemporain-pf1415.html",
        # "http://www.sothebys.com/en/auctions/2014/old-master-sculpture-works-art-l14233.html",
        # "http://www.sothebys.com/en/auctions/2014/schweizer-kunst-swiss-art-zh1406.html",
        # "http://www.sothebys.com/en/auctions/2014/books-manuscripts-n09237.html",
        # "http://www.sothebys.com/en/auctions/2014/medieval-renaissance-manuscripts-l14241.html",
        # "http://www.sothebys.com/en/auctions/2015/magnificent-jewels-n09331.html",
        # "http://www.sothebys.com/en/auctions/2014/american-art-n09148.html",
        # "http://www.sothebys.com/en/auctions/2014/19th-century-european-art-n09143.html",
        # "http://www.sothebys.com/en/auctions/2014/chinese-lacquer-from-baoyizhai-collection-part-i-hk0544.html",
        # "http://www.sothebys.com/en/auctions/2014/fine-chinese-ceramics-works-of-art-hk0517.html",
        # "http://www.sothebys.com/en/auctions/2014/contemporary-art-day-sale-n09142.html",
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-evening-sale-n09139.html",
        # "http://www.sothebys.com/en/auctions/2014/art-impressionniste-et-moderne-pf1406.html",
        # "http://www.sothebys.com/en/auctions/2014/bibliotheque-r-bl-pf1453.html" --,
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-n09140.html",
        # "http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-n09220.html",
        # "http://www.sothebys.com/en/auctions/2014/old-master-british-paintings-day-l14037.html",
        # "http://www.sothebys.com/en/auctions/2014/indiana-historical-society-audubon-n09133.html",
        # "http://www.sothebys.com/en/auctions/2014/waldorf-collection-n09131.html" --,
        # "http://www.sothebys.com/en/auctions/2014/made-in-britain-l14144.html",
        # "http://www.sothebys.com/en/auctions/2014/exploration-discovery-library-franklin-brooke-hitching-l14411.html" --,
        # "http://www.sothebys.com/en/auctions/2014/chinese-paintings-hk0516.html",
        # "http://www.sothebys.com/en/auctions/2014/american-paintings-drawings-sculpture-n09125.html"
        # "http://www.sothebys.com/en/auctions/2014/the-new-york-sale-n09215.html",
        # "http://www.sothebys.com/en/auctions/2015/private-collection-of-important-wines-hk0621.html",
        # "http://www.sothebys.com/en/auctions/2014/20th-century-chinese-art-hk0498.html",
        # "http://www.sothebys.com/en/auctions/2014/modern-contemporary-southeast-asian-paintings-hk0529.html"
        # "http://www.sothebys.com/en/auctions/2014/contemporary-asian-art-hk0497.html",
        # "http://www.sothebys.com/en/auctions/2014/fine-jewels-l14050.html"
        # "http://www.sothebys.com/en/auctions/2015/important-jewels-n09310.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-art-evening-auction-l15020.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-art-day-auction-l15021.html",
        # "http://www.sothebys.com/en/auctions/2015/collections-ducs-rochechouart-mortemart-pf1529.html",
        # "http://www.sothebys.com/en/auctions/2015/one-in-eleven-l15018.html",
        # "http://www.sothebys.com/en/auctions/2015/of-royal-and-noble-descent-l15306.html",
        # "http://www.sothebys.com/en/auctions/2015/important-20th-c-design-n09315.html",
        # "http://www.sothebys.com/en/auctions/2015/contemporary-curated-n09316.html",
        # "http://www.sothebys.com/en/auctions/2015/bande-dessinee-pf1555.html",
        # "http://www.sothebys.com/en/auctions/2015/so-peter-lewis-n09324.html",
    ]

    def parse(self, response):
        """
        This parse recover only data to populate the aste information

        """
        # open('aste.html', 'wb').write(response.body)

        items = []
        sel = Selector(response)
        link_next = sel.xpath("//div[@class='topmenu-inner-wrap']/a[@class='preferred logged-out']/@href").extract()
        print "LINK_NEXT: %s" % (link_next)

        # pp = len(sel.xpath("//span[@class='location']/text()").extract())
        urls = len(self.start_urls)
        print "Url Investigate: %s" % urls
        # --

        for p in range(0, urls):
            item = AsteWebsite()

            pathlink = urlparse(self.start_urls[p])
            item["linkurl"] = pathlink.path
            # item['linkurl'] = link_next
            print "PRIMO LINKURL: %s" % item["linkurl"]
            # i need to scan multiple article class
            # here for documentation :
            # http://doc.scrapy.org/en/latest/topics/selectors.html
            item['location'] = response.css('p.paragraph-module_paragraph18Regular__34C1i.css-cgm4gv::text')[5].extract()[3:].strip().encode("utf-8")

            pathlink = urlparse(self.start_urls[p])
            if not item["linkurl"]:
                item["linkurl"] = pathlink.path
            print "SECONDO LINKURL: %s" % item["linkurl"]
            item['downloadhref'] = response.css('div.css-17ddsqm img::attr(src)').extract()[0].strip()
            #item["downloadhref"] = (
            #    self.start_urls[p]
            #    .replace("http://www.sothebys.com", "")
            #    .replace("/en/auctions/", "/en/auctions/ecatalogue/")
            #    .replace(".html", "/")
            #)

            import datetime
            ###datetime.datetime.strptime('01 July 2015',"%d %B %Y").date()
            cnvrtdate = sel.xpath("//*[@id='x-event-date']/text()").extract()#[0].strip()
            item["date"] = response.css('p.paragraph-module_paragraph18Regular__34C1i.css-cgm4gv::text').extract()[3].strip().encode("utf-8")
            item["datafine"] = item["date"]
            item["name"] = (
                sel.xpath("/html/head/title/text()")
                .extract()[0]
                .encode("ascii", "ignore")
                .replace("|", "")
                .replace("Sotheby's", "")
                .strip()
            )
            item["category"] = "not cat"
            try:
                item["overview"] = response.css('div.css-1kakqgq>p::text')[1].extract().strip()
            except BaseException:
                item["overview"] = "no overview"

            item["asta"] = self.name
            try:
                item["maxlot"] = response.css('span.css-kajn87-label-book::text')[0].extract()[:4].strip()
            except BaseException:
                item["maxlot"] = ""

            item["sales_number"] = response.css('div.css-1kakqgq>p::text')[0].extract()[4:].strip()
            try:
                item["layout"] = "layout"
            except BaseException:
                item["layout"] = "not layout"
            # the first run is with flag 'Q'. It then is updated with value C in (parse_lot_sales_date) if all is ok
            # otherwiese remain with Q = Quarantena status
            item["status"] = "C"
            try:
                item["sale_total"] = sel.xpath(
                    "//div[@class='eventdetail-headerresults']/div/span/text()"
                ).extract()[0]
            except BaseException:
                # pass
                item["sale_total"] = "0"

            lotpage = self.start_urls[p]
            # open('aste.html', 'wb').write(response.body)
            print "LOTPAGE: %s" % (lotpage)
            # print 'ASTA: %s' % self.name
            # print "Date : %s" % (item['date'])
            # item['image'] = sel.xpath("//div[@class='image']//img/@serc").extract()

            # items.append(item)

            ##next_page = [('http://www.sothebys.com' + str(lotpage))]
            next_page = [(lotpage)]
            # if not not next_page:
            print "NEXTPAGEE: %s" % next_page
            #items.append(Request(next_page[0], self.parse_lot_sales_data))

            items.append(item)
            xx = len(items)
            # print 'XXX: %s' % xx

        return items

    def parse_lot_sales_data(self, response):
        """
        This function has the task to recover three field information
        to complete informations about t.aste, fields are
        .. - maxlot
        .. - sales number
        .. - date event
        .. - status

        One time firlds are recovery, they are updated in the table t.aste
        """
        # open('lots_ales_data.html', 'wb').write(response.body)
        print "RESPONSE: %s" % response
        items = []
        sel = Selector(response)

        item = AsteWebsite()
        image_relative_urls = sel.xpath(
            '//div[@class="zoom-hover-trigger"]//img/@src'
        ).extract()

        # [name] - Questo campo e' molto importante, infatti viene utilizzato per creare una chiave assoluta e
        # univoca da inserire in t.aste.guid job da eseguire in pipeline.py
        # TO DO  BUGS: In some cases the name is splitted on two row. While the insert rules is ok for name
        # here the name copy only the first parte of real name. Open a
        # Workaround near this bugs
        item["name"] = (
            sel.xpath("/html/head/title/text()")
            .extract()[0]
            .encode("ascii", "ignore")
            .replace("|", "")
            .replace("Sotheby's", "")
            .strip()
        )
        # item['name'] = sel.xpath("//div[@class='eventdetail-headerleft']/h1/text()").extract()[0].encode("ascii","ignore").strip()

        # item['name'] = sel.xpath("//ul[@class='breadcrumb inline']/li/a/span/text()").extract()

        # [maxlot] - Riflette il numero complessivo dei lotti che compongono l'asta.
        # questo dato va aggiornato nella tabella t.aste.maxlot
        try:
            item["maxlot"] = response.css('span.css-kajn87-label-book::text')[0].extract()[:4].strip()
        except BaseException:
            item["maxlot"] = ""
            # pass

        # [sales_number] - Riporta il numero di sala dell asta.
        # questo dato va aggiornato nella tabella t.aste.sales_number
        item["sales_number"] = response.css('div.css-1kakqgq>p::text')[0].extract()[4:].strip()
        try:
            item["sale_total"] = sel.xpath(
                "//div[@class='eventdetail-headerresults']/div/span/text()"
            ).extract()[0]
        except BaseException:
            item["sale_total"] = "0"
        item["asta"] = self.name
        item["date"] = response.css('p.paragraph-module_paragraph18Regular__34C1i.css-cgm4gv::text').extract()[0].strip().encode("utf-8")
        #item["date"] = sel.xpath("//*[@id='x-event-date']/text()").extract()#[0].strip()
        item["datafine"] = item["date"]
        item["category"] = "not cat"
        try:
            item["overview"] = response.css('div.css-1kakqgq>p::text')[1].extract().strip()
        except BaseException:
            item["overview"] = "no overview"

        item['location'] = response.css('p.paragraph-module_paragraph18Regular__34C1i.css-cgm4gv::text')[5].extract()[3:].strip().encode("utf-8")
        item["status"] = "C"

        item["downloadhref"] = (
            self.start_urls[0]
            .replace("http://www.sothebys.com", "")
            .replace("/en/auctions/", "/en/auctions/ecatalogue/")
            + "/lot.1.html"
        )
        item["layout"] = "layout"

        try:
            item["linkurl"] = sel.xpath(
                "//div[@class='description']/a/@href"
            ).extract()[0]
        except IndexError:
            item["linkurl"] = str(urlparse(self.start_urls[0]))
        print "TERZO LINKURL: %s" % item["linkurl"]
        # item['linkurl'] = self.start_urls

        link = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()
        # next_page = [('http://www.sothebys.com' + str(lotpage))]
        # if not not next_page:
        # items.append(Request("http://www.sothebys.com/en/auctions/ecatalogue/2014/collections-l14305/lot.1.html", callback=self.parse_opere))

        items.append(item)

        return items
