import cherrypy
import redis
from mako.template import Template
import os


class DisplayScrape(object):
    @cherrypy.expose
    def index(self):
	template = Template(filename="views/display_scraped_data.html")  #Load template file
	conn = redis.Redis('localhost') #connect to redis 
	d = conn.hgetall("pythonDict") # Get dictionary pythonDict stored in redis
	d = {int(k):v.replace("[","").replace("]","").split("','")[0].split("', '")  for k,v in d.items()}  # All keys and values of dictionary d will be in string format you need convert them to int and list
	html = template.render(mydata=d)  #Render To template file
	return html # Return HTML to be displayed
if __name__ == '__main__':
	cherrypy.server.socket_host = '0.0.0.0' # Tell cherryPy to run  in 0.0.0.0 to give remote access
	current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep # gives current_directory
#	print current_dir
	config = { #Cconfiguration 
		    'global': {
		'environment': 'production',
       	 'log.screen': True,
	        'server.socket_host': '0.0.0.0', # Tell cherryPy to run  in 0.0.0.0 to give remote access
	        'server.socket_port': 8080, # Tell cherryPy to run app in 8080 port
	        'engine.autoreload_on': True,
	        'log.error_file': os.path.join(current_dir, 'errors.log'),  # set the error logs file
	        'log.access_file': os.path.join(current_dir, 'access.log'), # access file
	    },
	    '/':{
	        'tools.staticdir.root' : current_dir,  # root of static directory
	    },
	    '/static':{
	        'tools.staticdir.on' : True,
	        'tools.staticdir.dir' : 'static', #name of static directory
	    },
		}
	cherrypy.quickstart(DisplayScrape(), '/', config)