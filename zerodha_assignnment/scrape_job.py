import os
from time import sleep
while 1:
	os.system("xvfb-run -a python scrape_table.py")
	sleep(60)