import urllib, mechanize
from mechanize import ParseResponse, urlopen, urljoin
import time
import simplejson
import os,sys
import csv
import time
from datetime import datetime, timedelta


import logging

import config

"""
Setup logger
"""
root = logging.getLogger()
root.setLevel(logging.INFO)

logger = logging.getLogger(config.log_file)
hdlr = logging.FileHandler(config.log_file+'.log')
log_format = '%(asctime)s %(levelname)s %(message)s'
formatter = logging.Formatter(log_format)
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


logger.info('Starting crawl of Chicago Card plus')



end_date = "10-01-2012"

if config.start_date:
  start_date = config.start_date
  start_date_time = datetime.strptime(start_date, "%m-%d-%Y")
  

if config.end_date:
  end_date = config.end_date
  end_date_time = datetime.strptime(end_date, "%m-%d-%Y")

if config.num_days:

  end_date_time  = datetime.now()
  end_date  = start_date_time.strftime("%m-%d-%Y")
  start_date_time = datetime.now() - timedelta(days=config.num_days)
  start_date = end_date_time.strftime("%m-%d-%Y")


delta = end_date_time - start_date_time

logger.info('start date: '+start_date)
logger.info('End date: '+end_date)
logger.info('Crawling '+str(delta.days)+" days")

if delta.days >90:
  logger.error("max 90 days data available. requesting "+str(delta.days)+" days. ")
  sys.exit(1)

br = mechanize.Browser()


"""
Login to CTA 
"""
logger.info("Logging in to CTA")
r = br.open(config.url_root)
params = {
    'hdrUSERNAME':config.email,
    'hdrPassword':config.password,

    }
data = urllib.urlencode(params)
r = br.open(config.url_root + "login-process.aspx", data)
page = r.read()
logger.info("Logged in to CTA")
"""
end logging
"""

logger.info("Parsing cards")

account_id =  page.split('<input name="AccountID" id="AccountID" type="hidden" value="')[1].split("\" />\r\n")[0]


logger.info("Account id: "+str(account_id))

cards_html = page.split('"></a><b class="acct-name">')


cards =[]
for c in cards_html:
  try:
     cards .append(c.split('TransactionHistoryEx.aspx?F_CTA_CARD=')[1].split('" class="view90">Export Last 90 Days')[0])
  except:
    pass

logger.info(str(len(cards))+" cards found: "+str(cards))


for c_id in cards:
  logger.info('Crawling card id #'+c_id)
  url = config.url_root + "/ccplus/TransactionHistoryEx.aspx?F_CTA_CARD="+c_id
  export_page = br.open(url).read()
  view_state= export_page.split('<input type="hidden" name="__VIEWSTATE" value="')[1].split("\" />\r\n")[0]
  file_name = 'cta_'+c_id+"_"+start_date+'_'+end_date+'.csv'

  params = {
      'AccountID':account_id,
      'F_CTA_CARD':c_id,
      'F_TRAN_DATE_FROM_MONTH':start_date_time.strftime("%m"),
      'F_TRAN_DATE_FROM_DAY':start_date_time.strftime("%d"),
      'F_TRAN_DATE_FROM_YEAR':start_date_time.strftime("%Y"),
      'F_TRAN_DATE_TO_MONTH':end_date_time.strftime("%m"),
      'F_TRAN_DATE_TO_DAY':end_date_time.strftime("%d"),
      'F_TRAN_DATE_TO_YEAR':end_date_time.strftime("%Y"),
      'F_TRAN_DISPLAY':"ALL",
      'Search':'Export',
      '__VIEWSTATE':view_state,

      }

  data = urllib.urlencode(params)
  r = br.open(url, data)

  csv_dump = r.read()
  logger.info('Dumping '+str(len(csv_dump.split("\n"))) +" lines")

  logger.info('writing data to '+file_name)
  f = open(file_name, 'w')
  f.write(csv_dump)
  f.closed

