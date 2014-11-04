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
    allowed_domains = ["sothebys.com"]
    start_urls = [
	#"http://www.sothebys.com/en/auctions.html#_charset_=utf-8&tzOffset=14400000&startDate=&endDate=&invertLocations=&eventTypes={e}AUC&showPast=false&resultSections=departments%3Blocations%3Btopics&filterExtended=true&search=&keywords=&lots=&ascing=asc&orderBy=date&lowPriceEstimateUSD=&highPriceEstimateUSD=&artists=&genres=&types=&mediums=&locations=&departments=&topics=&currency=USD&part=true&from=0&to=12&isAuthenticated=false",
        "http://www.sothebys.com/en/auctions.html",
    ]

    def parse(self, response):
        """
        This parse recover only data to populate the aste information

        """
	#open('aste.html', 'wb').write(response.body)
    	
    	items = []
    	sel = Selector(response)
	## search after a method for this
    	link_next = sel.xpath("//div[@class='topmenu-inner-wrap']/a[@class='preferred logged-out']/@href").extract()
	#print "LINK_NEXT: %s" % (link_next)
	
	current_page = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[0]
	element_onpage = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[2]
	tot_page = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[4]
        print "************************************************:dmoz"
	print "CURRENT_PAGE: %s" % (current_page)
	print "ELEMENT_ONPAGE: %s" % (element_onpage)
	print "TOT_PAGE: %s" % (tot_page)
	print self.name
    	
	pp = len(sel.xpath("//span[@class='location']/text()").extract())
        #--
	
	for p in range(0,pp):
            item = AsteWebsite()

	    item['linkurl'] = link_next
	    ## i need to scan multiple article class
            ## here for documentation : http://doc.scrapy.org/en/latest/topics/selectors.html 
            item['location'] = sel.xpath("//span[@class='location']/text()").extract()[p].encode('utf-8').strip()
            item['linkurl'] = sel.xpath("//div[@class='description']/a/@href").extract()[p]
	    ## this field keep an url page of asta; it server on pagelot download function
	    item['downloadhref'] = sel.xpath("//*[@id='eventdetail-carousel']/ul/li[2]/a/@href").extract()
            item['date'] = sel.xpath("//div[@class='vevent']/time/text()").extract()[p]
            item['name'] = sel.xpath("//div[@class='description']/a/text()").extract()[p].encode('ascii','ignore').strip()
	    item['asta'] = self.name
	    item['maxlot'] = 0
	    item['sales_number'] = 0
	    ## the first run is with flag 'Q'. It then is updated with value C in (parse_lot_sales_date) if all is ok
	    ## otherwiese remain with Q = Quarantena status 
	    item['status'] = "Q"
	    item['sale_total'] = 0
            lotpage = item['linkurl'] = sel.xpath("//div[@class='description']/a/@href").extract()[p]
	    
	    open('aste.html', 'wb').write(response.body)
	    #print 'LOTPAGE: %s' % (lotpage)
	    #print "Date : %s" % (item['date'])
            #item['image'] = sel.xpath("//div[@class='image']//img/@serc").extract()

	    items.append(item)
	    
	    next_page = [('http://www.sothebys.com' + str(lotpage))]
    	    #if not not next_page:
	    items.append(Request(next_page[0], self.parse_lot_sales_data))

	    items.append(item)
	    xx = len(items)
	    print 'XXX: %s' % xx
	    #mailer.send(to=["info@artecielo.com"], subject="Aste Inserite", body="Di seguito le aste inserite:\n"+ str([items[1]['asta'] for dd in range(xx)], cc=["teseo@broletto.org"])
	    #mailer.send(to=["marco.giardina@gmail.com"], subject="Aste Inserite", body="Di seguito le aste inserite:\n"+str(items[0]['asta'])+"\n"+str(items[0]['name']), cc=["teseo@broletto.org"])
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
	open('lots_ales_data.html', 'wb').write(response.body)
	print 'RESPONSE: %s' % response
        items = []
	sel = Selector(response)
	
        item = AsteWebsite()
	image_relative_urls = sel.xpath('//div[@class="zoom-hover-trigger"]//img/@src').extract()

	##[name] - Questo campo e' molto importante, infatti viene utilizzato per creare una chiave assoluta e 
	# univoca da inserire in t.aste.guid job da eseguire in pipeline.py
	## TO DO  BUGS: In some cases the name is splitted on two row. While the insert rules is ok for name
        ## here the name copy only the first parte of real name. Open a Workaround near this bugs 
	item['name'] = sel.xpath("//div[@class='eventdetail-headerleft']/h1/text()").extract()[1].strip()
 
	#item['name'] = sel.xpath("//ul[@class='breadcrumb inline']/li/a/span/text()").extract()

	##[maxlot] - Riflette il numero complessivo dei lotti che compongono l'asta.
        ##questo dato va aggiornato nella tabella t.aste.maxlot
        item['maxlot'] = sel.xpath("//div[@class='eventdetail-saleinfo']/span/text()").extract()[1].split()[2]
	    
	##[time] - Riporta l'ora dell'evento asta.
        #[TO DO] - Non ancora incorporato nella tabella aste
        ##questo dato va aggiornato nella tabella t.aste.time
        ##item['time'] = sel.xpath("//div[@class='eventdetail-eventtime']/time/text()").extract()[1].strip()
	item['sale_total'] = sel.xpath("//div[@class='eventdetail-headerresults']/div/span/text()").extract()

	##[sales_number] - Riporta il numero di sala dell asta.
        ##questo dato va aggiornato nella tabella t.aste.sales_number
        item['sales_number'] = sel.xpath("//div[@class='eventdetail-saleinfo']/span/text()").extract()[0].split()[2]

        ##[status] update the status asta [C] = Calendar [A] = Analize [R] = Result [P] = Publication
	item['status'] = "C"

	##[downloadhref] This is the official href link to initial download lot for asta name. Here is 
	## i update
	item['downloadhref'] = sel.xpath("//*[@id='eventdetail-carousel']/ul/li[2]/a/@href").extract()[0]

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
	open('opere.html', 'wb').write(response.body)

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
	open('test.html', 'wb').write(response.body)

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
            item['date'] = sel.xpath("//div[@class='lotdetail-artist-dates']/text()").extract()

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
