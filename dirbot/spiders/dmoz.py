from scrapy.spider import Spider, BaseSpider
from scrapy.selector import Selector

from dirbot.items import Website

from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import *

class DmozSpider(BaseSpider):
    name = "sothebys"
    allowed_domains = ["sothebys.com"]
    start_urls = [
	#"http://www.sothebys.com/en/auctions/2014/old-master-british-drawings-l14040.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/old-master-british-drawings-l14040/lot.1.html",
	"http://www.sothebys.com/en/auctions/ecatalogue/2014/20th-century-italian-art-l14624/lot.12.html",
	#"http://www.sothebys.com/it/auctions/ecatalogue/2014/contemporary-art-day-auction-l14023/lot.101.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/joseph-conrad-so-l14415/lot.194.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/english-literature-history-childrens-books-illustrations-l14404/lot.401.html",
	#"http://www.sothebys.com/en/auctions/ecatalogue/2014/fine-jewels-l14051/lot.1.html",
        #"http://www.sothebys.com/en/auctions/ecatalogue/2014/20th-century-italian-art-l14624/lot.1.html"
    ]

    #def parse(self, response):
    	
    #    items = []
    #	sel = Selector(response)
    #	#cp_link_image = sel.xpath("//div[@class='image']/a[@class='image']/@href").extract()
    #	cp_link_image = sel.xpath("//a/@href").extract()
    #	next_page = "http://www.sothebys.com"+str(cp_link_image).strip()
     	#return Request("http://www.sothebys.com/en/auctions/ecatalogue/2014/old-master-british-drawings-l14040/lot.1.html",
        #                  callback=self.parse_opere)
    #	return Request(str(next_page), callback=self.parse_opere)

    def parse(self, response):
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
