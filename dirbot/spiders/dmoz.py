from scrapy.spider import Spider, BaseSpider
from scrapy.selector import Selector

from dirbot.items import Website, AsteWebsite

from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy import *
from scrapy.mail import MailSender

mailer = MailSender()
#mailer.send(to=["marco.giardina@gmail.com"], subject="Some subject", body="Some body", cc=["info@mammagatto.org"])

class DmozSpider(BaseSpider):
    name = "sothebys"
    
    def __init__(self, facility=None, *args, **kwargs):
        super(DmozSpider, self).__init__(*args, **kwargs)
        #self.start_urls = ['http://www.example.com/categories/%s' % category]

        ## introduce facility costructor
        #@ facility is:
        #@ - more start_urls = 1 
        #@ - custom category = 2
        #@ - single asta = 3

        #@ for example:
        #@ scrapy crawl sothebys -a facility=1 [ -a domain=system]
  
    allowed_domains = ["sothebys.com"]
    start_urls = [
	"http://www.sothebys.com/en/auctions/2015/magnificent-jewels-n09331.html",
	#"http://www.sothebys.com/en/auctions/2014/american-art-n09148.html",
	#"http://www.sothebys.com/en/auctions/2014/19th-century-european-art-n09143.html",
	#"http://www.sothebys.com/en/auctions/2014/chinese-lacquer-from-baoyizhai-collection-part-i-hk0544.html",
	#"http://www.sothebys.com/en/auctions/2014/fine-chinese-ceramics-works-of-art-hk0517.html",
	#"http://www.sothebys.com/en/auctions/2014/contemporary-art-day-sale-n09142.html",
	#"http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-evening-sale-n09139.html",
	#"http://www.sothebys.com/en/auctions/2014/art-impressionniste-et-moderne-pf1406.html",
	#"http://www.sothebys.com/en/auctions/2014/bibliotheque-r-bl-pf1453.html" --,
	#"http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-n09140.html",
	#"http://www.sothebys.com/en/auctions/2014/impressionist-modern-art-day-sale-n09220.html",
	#"http://www.sothebys.com/en/auctions/2014/old-master-british-paintings-day-l14037.html",
	#"http://www.sothebys.com/en/auctions/2014/indiana-historical-society-audubon-n09133.html",
	#"http://www.sothebys.com/en/auctions/2014/waldorf-collection-n09131.html" --,
	#"http://www.sothebys.com/en/auctions/2014/made-in-britain-l14144.html",
	#"http://www.sothebys.com/en/auctions/2014/exploration-discovery-library-franklin-brooke-hitching-l14411.html" --,
	#"http://www.sothebys.com/en/auctions/2014/chinese-paintings-hk0516.html",
	#"http://www.sothebys.com/en/auctions/2014/american-paintings-drawings-sculpture-n09125.html"
	#"http://www.sothebys.com/en/auctions/2014/the-new-york-sale-n09215.html",
	#"http://www.sothebys.com/en/auctions/2015/private-collection-of-important-wines-hk0621.html",
	#"http://www.sothebys.com/en/auctions/2014/20th-century-chinese-art-hk0498.html",
	#"http://www.sothebys.com/en/auctions/2014/modern-contemporary-southeast-asian-paintings-hk0529.html"
	#"http://www.sothebys.com/en/auctions/2014/contemporary-asian-art-hk0497.html",
	#"http://www.sothebys.com/en/auctions/2014/fine-jewels-l14050.html"
        #"http://www.sothebys.com/en/auctions/2015/important-jewels-n09310.html",
        #"http://www.sothebys.com/en/auctions/2015/contemporary-art-evening-auction-l15020.html",
	#"http://www.sothebys.com/en/auctions/2015/contemporary-art-day-auction-l15021.html",
	#"http://www.sothebys.com/en/auctions/2015/collections-ducs-rochechouart-mortemart-pf1529.html",
	#"http://www.sothebys.com/en/auctions/2015/one-in-eleven-l15018.html",
	#"http://www.sothebys.com/en/auctions/2015/of-royal-and-noble-descent-l15306.html",
	#"http://www.sothebys.com/en/auctions/2015/important-20th-c-design-n09315.html",
	#"http://www.sothebys.com/en/auctions/2015/contemporary-curated-n09316.html",
	#"http://www.sothebys.com/en/auctions/2015/bande-dessinee-pf1555.html",
	#"http://www.sothebys.com/en/auctions/2015/so-peter-lewis-n09324.html",
    ]

    def parse(self, response):
        """
        This parse recover only data to populate the aste information

        """
	#open('aste.html', 'wb').write(response.body)
    	
    	items = []
    	sel = Selector(response)
    	link_next = sel.xpath("//div[@class='topmenu-inner-wrap']/a[@class='preferred logged-out']/@href").extract()
	#print "LINK_NEXT: %s" % (link_next)
	
	#current_page = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[0]
	#element_onpage = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[2]
	#tot_page = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[4]
        print "************************************************:dmoz"
	#print "CURRENT_PAGE: %s" % (current_page)
	#print "ELEMENT_ONPAGE: %s" % (element_onpage)
	#print "TOT_PAGE: %s" % (tot_page)
	print self.start_urls
    	
	#pp = len(sel.xpath("//span[@class='location']/text()").extract())
	pp = len(self.start_urls)
	print 'PPPPP: %s' % pp
        #--

	for p in range(0,1):
            item = AsteWebsite()

	    item['linkurl'] = link_next
	    ## i need to scan multiple article class
            ## here for documentation : http://doc.scrapy.org/en/latest/topics/selectors.html 
            #item['location'] = sel.xpath("//span[@class='location']/text()").extract()[p].encode('utf-8').strip()
            #item['location'] = sel.xpath("//*[@id='bodyWrap']/div[2]/div[3]/div[2]/div[1]/div[2]/ul/li/div/h3/text()").extract()[p].encode('ascii','ignore').strip()
	    try:
                item['location'] = sel.xpath("//*[@id='bodyWrap']/div[2]/div[3]/div[2]/div[1]/div[1]/ul/li/div/h3/text()").extract()[p].encode('ascii','ignore').strip()
	    except:
		#item['location'] = sel.xpath("//*[@id='bodyWrap']/div[2]/div[3]/div[2]/div[1]/div[2]/ul/li/div/h3/text()").extract()[0]
		#item['location'] = sel.xpath("//*[@id='bodyWrap']/div[2]/div[3]/div[2]/div[1]/div[2]/ul/li/div/h3/text()").extract()
		item['location'] = sel.xpath("//span[@class='location']/text()").extract()[:1][0].strip()

            #item['linkurl'] = sel.xpath("//div[@class='description']/a/@href").extract()[p]
            item['linkurl'] = self.start_urls[p].replace("http://www.sothebys.com","")
	    ## this field keep an url page of asta; it server on pagelot download function
	    #item['downloadhref'] = sel.xpath("//*[@id='eventdetail-carousel']/ul/li[2]/a/@href").extract()
	    #item['downloadhref'] = self.start_urls[p].replace("http://www.sothebys.com","").replace("/en/auctions/","/en/auctions/ecatalogue/").replace(".html","")+"/lot.1.html"
	    item['downloadhref'] = self.start_urls[p].replace("http://www.sothebys.com","").replace("/en/auctions/","/en/auctions/ecatalogue/").replace(".html","/")
            #item['date'] = sel.xpath("//div[@class='vevent']/time/text()").extract()[p]
            item['date'] = sel.xpath("//*[@id='x-event-date']/text()").extract()[0].strip()
            #item['name'] = sel.xpath("//div[@class='description']/a/text()").extract()[p].encode('ascii','ignore').strip()
	    #item['name'] = sel.xpath("//div[@class='description']/a/text()").extract()[p].encode('ascii','ignore').strip()
	    item['name'] = sel.xpath("/html/head/title/text()").extract()[0].encode('ascii','ignore').replace("|","").replace("Sotheby's","").strip()
	   
	    item['asta'] = self.name
	    try:
                item['maxlot'] = sel.xpath("//div[@class='eventdetail-saleinfo']/span/text()").extract()[1].split()[2]
	    except:
	        item['maxlot'] = 0
            item['sales_number'] = sel.xpath("//div[@class='eventdetail-saleinfo']/span/text()").extract()[0].split()[2]
	    #item['sales_number'] = 0
            try:
	        item['layout'] = facility
	    except:
	        item['layout'] = ''
	    ## the first run is with flag 'Q'. It then is updated with value C in (parse_lot_sales_date) if all is ok
	    ## otherwiese remain with Q = Quarantena status 
	    item['status'] = "C"
	    try:
	        item['sale_total'] = sel.xpath("//div[@class='eventdetail-headerresults']/div/span/text()").extract()[0]
	    except:
	        item['sale_total'] = 0
            #lotpage = item['linkurl'] = sel.xpath("//div[@class='description']/a/@href").extract()[p]
            #lotpage = item['linkurl'] = self.start_urls[p]
            lotpage = self.start_urls[p]
	    
	    #open('aste.html', 'wb').write(response.body)
	    print 'LOTPAGE: %s' % (lotpage)
	    print 'ASTA: %s' % self.name
	    #print "Date : %s" % (item['date'])
            #item['image'] = sel.xpath("//div[@class='image']//img/@serc").extract()

	    items.append(item)
	    
	    ##next_page = [('http://www.sothebys.com' + str(lotpage))]
	    next_page = [(lotpage)]
    	    #if not not next_page:
    	    print 'NEXTPAGEE: %s' % next_page
	    items.append(Request(next_page[0], self.parse_lot_sales_data))

	    items.append(item)
	    xx = len(items)
	    print 'XXX: %s' % xx

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
	#open('lots_ales_data.html', 'wb').write(response.body)
	print 'RESPONSE: %s' % response
        items = []
	sel = Selector(response)
	
        item = AsteWebsite()
	image_relative_urls = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()

	##[name] - Questo campo e' molto importante, infatti viene utilizzato per creare una chiave assoluta e 
	# univoca da inserire in t.aste.guid job da eseguire in pipeline.py
	## TO DO  BUGS: In some cases the name is splitted on two row. While the insert rules is ok for name
        ## here the name copy only the first parte of real name. Open a Workaround near this bugs 
	item['name'] = sel.xpath("//div[@class='eventdetail-headerleft']/h1/text()").extract()[1].encode("ascii","ignore").strip()
 
	#item['name'] = sel.xpath("//ul[@class='breadcrumb inline']/li/a/span/text()").extract()

	##[maxlot] - Riflette il numero complessivo dei lotti che compongono l'asta.
        ##questo dato va aggiornato nella tabella t.aste.maxlot
	try:
            item['maxlot'] = sel.xpath("//div[@class='eventdetail-saleinfo']/span/text()").extract()[1].split()[2]
	except:
	    item['maxlot']=0
	    
	##[time] - Riporta l'ora dell'evento asta.
        #[TO DO] - Non ancora incorporato nella tabella aste
        ##questo dato va aggiornato nella tabella t.aste.time
        ##item['time'] = sel.xpath("//div[@class='eventdetail-eventtime']/time/text()").extract()[1].strip()
	item['sale_total'] = sel.xpath("//div[@class='eventdetail-headerresults']/div/span/text()").extract()[0]
	#item['sale_total'] = [xx for xx in sel.xpath("//div[@class='eventdetail-headerresults']/div/span/text()").extract()[0]]
	#if not item['sale_total']:
	#	item['sale_total'] = 0
	#[x+1 if x >= 45 else x+5 for x in l]

	##[sales_number] - Riporta il numero di sala dell asta.
        ##questo dato va aggiornato nella tabella t.aste.sales_number
        item['sales_number'] = sel.xpath("//div[@class='eventdetail-saleinfo']/span/text()").extract()[0].split()[2]

        ##[status] update the status asta [C] = Calendar [A] = Analize [R] = Result [P] = Publication
	item['status'] = "C"

	##[downloadhref] This is the official href link to initial download lot for asta name. Here is 
	## i update
	#item['downloadhref'] = sel.xpath("//*[@id='eventdetail-carousel']/ul/li[2]/a/@href").extract()[0]
	item['downloadhref'] = self.start_urls
	#item['downloadhref'] = self.start_urls.replace("http://www.sothebys.com","").replace("/en/auctions/","/en/auctions/ecatalogue/").replace(".html","")+"/lot.1.html"
	#item['downloadhref'] = self.start_urls[p].replace("http://www.sothebys.com","").replace("/en/auctions/","/en/auctions/ecatalogue/")+"/lot.1.html"
	item['layout'] = facility
	
	item['linkurl'] = self.start_urls

	link = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()
	#next_page = [('http://www.sothebys.com' + str(lotpage))]
    	#if not not next_page:
	#items.append(Request("http://www.sothebys.com/en/auctions/ecatalogue/2014/collections-l14305/lot.1.html", callback=self.parse_opere))

        items.append(item)
	
        return items

    def parse_opere(self, response):
        """
        This fuction adds records on the t.opere:
        It bring the t.aste.linkurl and scan the full three page. At the end
	if lot number is equala at t.aste.maxlot sent a mail at info at artecielo dot com

        """
	#open('opere.html', 'wb').write(response.body)

        items = []
	sel = Selector(response)

	#this is the nex link of asta
	link_next = sel.xpath("//div[@class='lot-navigation lotdetail-navigation']/a[@class='arrow-right']/@href").extract()[0]
	next_page = [('http://www.sothebys.com' + str(link_next))]
	print "NEXTOPERA; %s" % next_page
    	if not not next_page:
		items.append(Request(next_page[0], self.parse))
	sites = sel.xpath("//div[@class='text-group span8']/h1[@class='number']/text()").extract()

        for site in sites:
	    print "ENTROOOOOOOOO"
            item = OpereWebsite()
	    image_relative_urls = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()

	    #item['linkurl'] = link_next

	    ##[maxlot] - Riflette il numero complessivo dei lotti che compongono asta.
            ##item['maxlot'] = sel.xpath("//div[@class='text-group']/h1[@class='number']/text()").extract()
            ##item['maxlot'] = link_next #sites
	    
	    ##[name] - Recupera il nome asta:ad ex. The Italian Sale
            item['name'] = sel.xpath("//span[@class='active']/text()").extract()[0]

	    ##[estimate] - Recupera il valore complessivo della casa di asta
            item['estimate'] = sel.xpath("//*[@id='bodyWrap']/div[4]/div/div[2]/section/div/div/div[2]/span[1]/text() | //*[@id='bodyWrap']/div[4]/div/div[2]/section/div/div/div[2]/span[2]/text()").extract()

	    ##[valuta] - Assegna la valuta predefinita all'opera
            item['valuta'] = sel.xpath("//*[@id='bodyWrap']/div[4]/div/div[2]/section/div/div/div[3]/div[1]/a/text()").extract()

	    ##[image_urls] - Il path principale della case d'aste dove risiedono dove risiedono  le immagini
            item['image_urls'] = sel.xpath("//*[@id='bodyWrap']/div[6]/div[2]/div[1]/div/div/img[1]/@src").extract()

	    ##[image] - Il nome della singola immagine
            item['images'] = sel.xpath("//*[@id='bodyWrap']/div[6]/div[2]/div[1]/div/div/img[1]/@src").extract()

            #item['notes'] = sel.xpath("//div[@class='notes']/div/h5/text()").extract()[0].strip()
            ##item['period'] = sel.xpath("//div[@class='text-group']/div/text()").extract()
            #item['title'] = sel.xpath("//div[@class='text-group']/h5[@class='div']/br/text()").extract()

	    ##[title] - Riflette il tittolo dell'opera dell'artista. Da inserire nella tabella OPERE(opere)
            item['title'] = sel.xpath("//*[@id='bodyWrap']/div[4]/div/div[2]/div/text()").extract()

            ##item['author'] = sel.xpath("//div[@class='text-group']/h5/text()").extract()
	    ##[author] - Rispecchia il nome dell'autore dell'opera. Deve essere inserito nella tabella OPERE(opere)
            ##item['author'] = sel.xpath("//div[@class='lotdetail-guarantee']/text()").extract()[:1][0].strip()
            #item['author'] = sel.xpath("//div[@class='lotdetail-guarantee']/text()").extract()

            item['description'] = sel.xpath("//*[@id='bodyWrap']/div[6]/div[6]/div/div[1]/div[1]/text()").extract()[0].strip().encode('ascii','ignore')
	    #link = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()[0]
	    #import urlparse 
	    #item['image_urls'] = [urlparse.urljoin(response.url, str(link))] 
	    #link = sel.xpath('//div[@class="zomm-hover-trigger"]//img/@src').extract()
    	    #item['image_urls'] = [('http://www.sothebys.com' + str(link))]

            items.append(item)

        return items

    def parse_aste(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
	#open('test.html', 'wb').write(response.body)

        items = []
	sel = Selector(response)
	link_next = sel.xpath("//div[@class='lot-navigation lotdetail-navigation']/a[@class='arrow-right']/@href").extract()[0]
    	#link_next = sel.xpath("//div[@class='lot-navigation']/a[@class='arrow-right']/@href").extract()
	next_page = [('http://www.sothebys.com' + str(link_next))]
    	if not not next_page:
		items.append(Request(next_page[0], self.parse))
	sites = sel.xpath("//div[@class='text-group span8']/h1[@class='number']/text()").extract()
        #sites = sel.xpath('//div[@class="text-group"]')
    	#link_next = sel.xpath("//div[@class='lot-navigation']/a[@class='arrow-right']/@href").extract()[0]
	#next_page = [('http://www.sothebys.com' + str(link_next))]
    	#if not not next_page:
	#	pass #return Request(next_page[0], self.parse)
        #items = []

        for site in sites:
            item = Website()
	    image_relative_urls = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()

	    item['linkurl'] = link_next

	    ##[maxlot] - Riflette il numero complessivo dei lotti che compongono asta.
            ##item['maxlot'] = sel.xpath("//div[@class='text-group']/h1[@class='number']/text()").extract()
            item['maxlot'] = link_next #sites
	    
	    ##[name] - Recupera il nome asta:ad ex. The Italian Sale
            item['name'] = sel.xpath("//span[@class='active']/text()").extract()

	    ##[date] - Questa rules Recupera la data di nascita dell'artista. Il dato va spostato in 
	    ##una futura tabella ARTISTI(artisti)
            #item['date'] = sel.xpath("//div[@class='lotdetail-artist-dates']/text()").extract()
            item['date'] = sel.xpath("//*[@id='x-event-date']/text()").extract()[0].strip()

	    ##[time] - Riflette l'ora dell'evento dell'asta. Il dato va inserito nella tabella ASTE(aste)
            item['time'] = sel.xpath("//div[@class='details vevent']/time/text()").extract()[0:2][1].strip()

	    ##[location] - Riflette la location(luogo) dell'evento dell'asta. ad ex. Londra. Il dato va inserito
	    ##nella tabella ASTE(aste)
            item['location'] = sel.xpath("//span[@class='location']/text()").extract()[:1][0].strip()

            #item['notes'] = sel.xpath("//div[@class='notes']/div/h5/text()").extract()[0].strip()
            ##item['period'] = sel.xpath("//div[@class='text-group']/div/text()").extract()
            #item['title'] = sel.xpath("//div[@class='text-group']/h5[@class='div']/br/text()").extract()

	    ##[title] - Riflette il tittolo dell'opera dell'artista. Da inserire nella tabella OPERE(opere)
            item['title'] = sel.xpath("//div[@class='lotdetail-subtitle']/text()").extract()[:1][0].strip()

            ##item['author'] = sel.xpath("//div[@class='text-group']/h5/text()").extract()
	    ##[author] - Rispecchia il nome dell'autore dell'opera. Deve essere inserito nella tabella OPERE(opere)
            item['author'] = sel.xpath("//div[@class='lotdetail-guarantee']/text()").extract()[:1][0].strip()
            #item['author'] = sel.xpath("//div[@class='lotdetail-guarantee']/text()").extract()

            #item['description'] = sel.xpath("//div[@class='description']/text()").extract()[0].encode('utf-8').strip()
            #item['description'] = u' '.join(sel.xpath("//div[@class='text-group']/div[@class='description']/text()").extract()[0]).encode('utf-8').strip()
            #item['description'] = sel.xpath("//div[@class='text-group']/div[@class='description']/text()").extract()[0].encode('utf-8').strip()
            ##item['description'] = str([word.strip().encode('utf-8') for word in sel.xpath("//div[@class='text-group']/div[@class='description']/text()").extract()])
            item['description'] = str([word.strip().encode('utf-8') for word in sel.xpath("//div[@class='lotdetail-catalogue-notes-holder']/text()").extract()])
            ##item['dimension'] = sel.xpath("//div[@class='lotdetail-description-text']/text()").extract()[0]
	    link = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()[0]
	    import urlparse 
	    #item['image_urls'] = [urlparse.urljoin(response.url, str(link))] 
	    #link = sel.xpath('//div[@class="zomm-hover-trigger"]//img/@src').extract()
    	    item['image_urls'] = [('http://www.sothebys.com' + str(link))]

            items.append(item)

        return items
