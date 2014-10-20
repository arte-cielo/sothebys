from scrapy.spider import Spider, BaseSpider
from scrapy.selector import Selector

from dirbot.items import Website, AsteWebsite

from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import *

class DmozSpider(BaseSpider):
    name = "sothebys"
    allowed_domains = ["sothebys.com"]
    start_urls = [
	"http://www.sothebys.com/en/auctions.html#_charset_=utf-8&tzOffset=14400000&startDate=&endDate=&invertLocations=&eventTypes={e}AUC&showPast=false&resultSections=departments%3Blocations%3Btopics&filterExtended=true&search=&keywords=&lots=&ascing=asc&orderBy=date&lowPriceEstimateUSD=&highPriceEstimateUSD=&artists=&genres=&types=&mediums=&locations=&departments=&topics=&currency=USD&part=true&from=0&to=12&isAuthenticated=false",
	#"http://www.sothebys.com/en/auctions/2014/old-master-british-drawings-l14040.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/old-master-british-drawings-l14040/lot.1.html",
        ##"http://www.sothebys.com/en/auctions/ecatalogue/2014/20th-century-italian-art-l14624/lot.12.html",
	#"http://www.sothebys.com/it/auctions/ecatalogue/2014/contemporary-art-day-auction-l14023/lot.101.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/joseph-conrad-so-l14415/lot.194.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/english-literature-history-childrens-books-illustrations-l14404/lot.401.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/fine-jewels-l14051/lot.1.html",
        #"http://www.sothebys.com/en/auctions/ecatalogue/2014/20th-century-italian-art-l14624/lot.1.html"
    ]

    def parse(self, response):
        """
        This parse recover only data to populate the aste information

        """
	open('aste.html', 'wb').write(response.body)
    	
    	items = []
    	sel = Selector(response)
	## search after a method for this
    	link_next = sel.xpath("//div[@class='topmenu-inner-wrap']/a[@class='preferred logged-out']/@href").extract()
	print "LINK_NEXT: %s" % (link_next)
	
	current_page = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[0]
	element_onpage = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[2]
	tot_page = sel.xpath("//span[@class='page-info']/text()").extract()[0].split()[4]
	print "CURRENT_PAGE: %s" % (current_page)
	print "ELEMENT_ONPAGE: %s" % (element_onpage)
	print "TOT_PAGE: %s" % (tot_page)

	loop = []
	pp = len(sel.xpath("//span[@class='location']/text()").extract())
	loop.append(pp -1)

	for p in range(0,pp):
            item = AsteWebsite()

	    item['linkurl'] = link_next
	    ## i need to scan multiple article class
            ## here for documentation : http://doc.scrapy.org/en/latest/topics/selectors.html 
            #item['date'] = sel.xpath("//time[@class='dtstart']/text()").extract()[0]
            #item['location'] = sel.xpath("//span[@class='location']/text()").extract()[:1][0].strip()
            item['location'] = sel.xpath("//span[@class='location']/text()").extract()[p].encode('utf-8').strip()
            item['time'] = sel.xpath("//div[@class='description']/a/@href").extract()[p]
            item['date'] = sel.xpath("//div[@class='vevent']/time/text()").extract()[p]
            #item['name'] = sel.xpath("//time/a/@href").extract()
            item['name'] = sel.xpath("//div[@class='description']/a/text()").extract()[p].encode('ascii','ignore').strip()
            #item['name'] = sel.xpath("//h4[@class='summary ellipsis']/text()").extract()
	    #print "Name : %s" % (item['name'].encode('utf-8').strip())
	    print "Date : %s" % (item['date'])
	    ## recover the link=>next or href that go on the page of details of the asta	
            #item['href'] = sel.xpath("//div[@class='image']/a/@href").extract()
            #item['time'] = sel.xpath("//div[@class='details vevent']/time/text()").extract)
	    ## load the image thumbnails of this page
            #item['image'] = sel.xpath("//div[@class='image']//img/@serc").extract()

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
