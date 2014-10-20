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
    name = Field()        # name asta. ad ex. The Italian Sale
    date = Field()        # date asta. ad ex. 17 Oct 2014
    asta = Field()        # name auction house. ad ex. Sothebys
    time = Field()        # this is teh time location. ad ex. 6.00 PB BEST
    location = Field()    # rapresent the location of event. ad ex. London . Milan
    maxlot = Field()      # rapresent the number of lots of catalogues.
    linkurl = Field()     # is a field that help to loop unique(hashkey)
