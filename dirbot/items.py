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
