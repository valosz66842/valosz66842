import time
import os
from datetime import datetime

while True:
    date = str(datetime.now()).replace('-','').replace(' ','').replace(':','').split('.')[0]
    os.system("scrapy crawl udn -o udn{}.json -t json".format(date))  # 取時間日期為檔名
    time.sleep(86400)  # 每隔一天執行一次 24*60*60=86400s