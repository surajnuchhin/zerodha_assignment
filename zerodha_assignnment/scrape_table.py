import sys  
from BeautifulSoup import BeautifulSoup
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
import redis
from time import sleep

class Scraper(QWebPage):  
	def __init__(self, url):  
		self.app = QApplication(sys.argv)   # create a browser APP
		QWebPage.__init__(self)             #Initialize web page
		self.loadFinished.connect(self._loadFinished)   #execute _loadFinished after loading is done
		self.mainFrame().load(QUrl(url))      # Load Url
		self.app.exec_()                      # Execute App
  
	def _loadFinished(self, result):  
		self.frame = self.mainFrame()       # Main frame is what contains return HTML 
		self.app.quit()                     # quit App

	def scrape_and_push(self) :
			result = self.frame.toHtml()  #Convert to Html
			formatted_result = str(result.toAscii())  # convert html to Ascii
			soup = BeautifulSoup(formatted_result)     #Beautiful Soup to parse HTML file
			table = soup.find(id="topGainers")   
			#print table     # find a table by name topGainers
	
			i=0
			dict={}
			for row in table.findAll('tr')[1:]:    # parse each element of table and create a dictionary
				col = row.findAll('td')
				#print len(col)
				if col[0].a != None :
					symbol_link = col[0].a['href']
					symbol = symbol_link.split("=")[1]
					ltp = col[1].string
					change_percent = col[2].string
					traded_qty = col[3].string
					traded_value = col[4].string
					open = col[5].string
					high = col[6].string
					low = col[7].string
					prev_close = col[8].string
					latest_exdate = col[9].string
					#print symbol_link, symbol, ltp, change_percent, traded_qty, traded_value, open, high, low, prev_close, latest_exdate
					dict[i] = [str(symbol_link), str(symbol), str(ltp), str(change_percent), str(traded_qty), str(traded_value), str(open), str(high), str(low),str( prev_close), str(latest_exdate)]
					i=i+1
			print "This is ",dict

			conn = redis.Redis('localhost')   #Open a connection with redis
			for key in conn.hgetall("pythonDict").keys() :
				conn.hdel("pythonDict",key)
			if len(dict) > 0 :
				conn.hmset("pythonDict", dict)    # Push data to redis

if __name__ == "__main__" :
	url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/top_gainers_losers.htm?cat=G' 
	try :
			sc = Scraper(url) #create an instance
			sc.scrape_and_push()	 # scrape and push Url
	except Exception as e :
			print "Error : ------",e
