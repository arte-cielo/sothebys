# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

#ITEM_PIPELINES = ['dirbot.pipelines.FilterWordsPipeline',
#		  'dirbot.pipelines.MyImagesPipeline',
#		  'dirbot.pipelines.MySQLStorePipeline',
#		 ]

#ITEM_PIPELINES = ['dirbot.pipelines.MyImagesPipeline',
#		  'dirbot.pipelines.MySQLStorePipeline',
#		 ]


ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1}
ITEM_PIPELINES = {'dirbot.pipelines.MyImagesPipeline': 1}
ITEM_PIPELINES = {'dirbot.pipelines.MySQLStorePipeline'}
#ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}

#IMAGES_STORE = '/home/sothebys/image'
IMAGES_STORE = '/home/grdnmrc/SOTHEBY/sothebys'
IMAGES_EXPIRES = 90

IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}

#IMAGES_MIN_HEIGHT = 40
#IMAGES_MIN_WIDTH = 40


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'dirbot.middlewares.ProxyMiddleware': 100,
}

MYSQL_HOST = '192.168.1.101'
MYSQL_DBNAME = 'artecielo'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'broletto'
MYSQL_PORT = '3306'
