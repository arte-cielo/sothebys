from scrapy.item import Item, Field


class Website(Item):
    author = Field()
    maxlot = Field()
    title = Field()
    description = Field()
    image_urls = Field()
    #images = Field()
    image_paths = Field()
    #period = Field()
    #dimension = Field()
    name = Field()
    date = Field()
    time = Field()
    location = Field()
    linkurl = Field()
    #notes = Field()


class AsteWebsite(Item):
    name = Field()          # name asta. ad ex. The Italian Sale
    date = Field()          # date asta. ad ex. 17 Oct 2014
    asta = Field()          # name auction house. ad ex. Sothebys
    time = Field()          # this is teh time location. ad ex. 6.00 PB BEST
    location = Field()      # rapresent the location of event. ad ex. London . Milan
    maxlot = Field()        # rapresent the number of lots of catalogues.
    sales_number = Field()  # is the sales number of teh room that sell lot.
    sale_total = Field()    # sum total of teh asta
    linkurl = Field()       # is a field that help to loop unique(hashkey)


class OpereWebsite(Item):
    asta = Field()          # asta foreign. This is the foreign key for guid Aste(2)
    title = Field()         # this is the Opera title. ad ex. Chateau Lafite 1986
    description = Field()   # this is the description area. Chateau Lafite 1986 Pauillac, 1er Cru Classe
    estimate = Field()      # report the value of lot
    lot_sold = Field()      # Sell lot
    valuta = Field()        # Valuta lot sell
    image_urls = Field()    # where to bring the image. 
    image_path = Field()    # the path where exist the image
    image = Field()         # this is the single image name ad ex. granoturco.jpg
    url = Field()           # not clear at the moment
    update_date = Field()   # operation date scrapy
