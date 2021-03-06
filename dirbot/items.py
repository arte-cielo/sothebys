from scrapy.item import Item, Field


class Website(Item):
    author = Field()
    maxlot = Field()
    title = Field()
    description = Field()
    image_urls = Field()
    # images = Field()
    image_paths = Field()
    # period = Field()
    # dimension = Field()
    name = Field()
    date = Field()
    time = Field()
    location = Field()
    linkurl = Field()
    # notes = Field()


class AsteWebsite(Item):
    name = Field()          # name asta. ad ex. The Italian Sale
    asta = Field()          # name auction house. ad ex. Sothebys
    date = Field()          # date asta. ad ex. 17 Oct 2014
    datafine = Field()      # data fine asta 12-12-2015
    category = Field()      # identifica la tipologia dell'asta 12-12-15
    overview = Field()      # breve descrizione asta
    linkurl = Field()       # is a field that help to loop unique(hashkey)
    downloadhref = Field()  # keep a href url to download teh page
    location = Field()      # rapresent the location of event. ad ex. London . Milan
    maxlot = Field()        # rapresent the number of lots of catalogues.
    layout = Field()        # keep idifferent layout for auction
    status = Field()        # is the sales number of teh room that sell lot.
    sales_number = Field()  # is the sales number of teh room that sell lot.
    sale_total = Field()    # sum total of teh asta
    update_date = Field()   # operation date scrapy
    time = Field()          # this is teh time location. ad ex. 6.00 PB BEST


## ================================================
## TO DO NEXT RELEAS: Inglobe cycle opere with aste
## ================================================
##class OpereWebsite(Item):
##    #asta = Field()          # asta foreign. This is the foreign key for guid Aste(2)
##    name = Field()          # actually this field make the key hash
##    title = Field()         # this is the Opera title. ad ex. Chateau Lafite 1986
##    description = Field()   # this is the description area. Chateau Lafite 1986 Pauillac, 1er Cru Classe
##    estimate = Field()      # report the value of lot
##    lot_sold = Field()      # Sell lot
##    valuta = Field()        # Valuta lot sell
##    image_urls = Field()    # where to bring the image.
##    image_path = Field()    # the path where exist the image
##    images = Field()        # this is the single image name ad ex. granoturco.jpg
##    url = Field()           # not clear at the moment
##    update_date = Field()   # operation date scrapy
