# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import requests
import traceback

from itertools import cycle
from lxml.html import fromstring

# Start your middleware class
class ProxyMiddleware(object):

    def get_proxies(self):
    	url = 'https://free-proxy-list.net/'
    	response = requests.get(url)
    	parser = fromstring(response.text)
    	proxies = set()
    	for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
    	return proxies

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        #request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
        #request.meta['proxy'] = "http://183.207.232.193:8080"
	proxies = self.get_proxies()
	proxy_pool = cycle(proxies)

	url = 'https://httpbin.org/ip'
	for i in range(1,11):
    	    #Get a proxy from the pool
    	    proxy = next(proxy_pool)
    	    print("Request #%d"%i)
    	    try:
        	response = requests.get(url,proxies={"http": proxy, "https": proxy})
        	print(response.json())
   	    except:
        	#Most free proxies will often get connection errors. You will have retry the entire 
		#request using another proxy to work. 
        	#We will just skip retries as its beyond the scope of this tutorial and we are only 
		#downloading a single url 
        	print("Skipping. Connnection error")

            # Use the following lines if your proxy requires authentication
            proxy_user_pass = "USERNAME:PASSWORD"
            # setup basic authentication for the proxy
            #encoded_user_pass = base64.encodestring(proxy_user_pass)
            #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

	    encoded_user_pass = base64.urlsafe_b64encode(proxy_user_pass.encode('UTF-8')).decode('ascii')
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
