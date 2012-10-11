#chicago card crawler
A crawler for the chicago card plus website. 


##Why
We need more data!

##How

open up a terminal

copy config.py.example to config.py: 

`$ cp config.py.example config.py`



edit config.py and fill out your info


	#enter dates if you want to crawl specific dates
	start_date = "08-01-2012"
	end_date = "10-01-2012"
	
	#enter the number of days you want to crawl (90 is the max)
	num_days = 90

	#username and password for chicago-card.com
	email = '' # username
	password = '' #passwd	
	
	#url root
	url_root = 'https://www.chicago-card.com/'
	
	#name of the logfile
	log_file = "CTA"
	
then run the script

`$ python chicago_card_crawler.py`
	
Magic

	INFO Starting crawl of Chicago Card plus
	INFO start date: 10-11-2012
	INFO End date: 08-01-2012
	INFO Crawling 4 days
	INFO Logging in to CTA
	INFO Logged in to CTA
	INFO Parsing cards
	INFO Account id: 176009
	INFO 2 cards found: ['1266731', '1392327']
	INFO Crawling card id #1266731
	INFO Dumping 10 lines
	INFO writing data to cta_1266731_10-11-2012_08-01-2012.csv
	INFO Crawling card id #1392327
	INFO Dumping 11 lines
	INFO writing data to cta_1392327_10-11-2012_08-01-2012.csv 
	
should work great!