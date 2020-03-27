import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import re
import urllib.parse
from opencc import OpenCC
import pandas as pd
import numpy as np
import jieba
import csv
cc = OpenCC('s2t')
FeatPath=r'E:\YoutubeYear\FeatDate.csv'
Feat_pd=pd.read_csv(FeatPath)
print(type(Feat_pd))
SortPd=Feat_pd.sort_values(by='FeatCount')
print(SortPd)
SortPd.to_csv('E:\YoutubeYear\FeatSortDate.csv',encoding='utf-8-sig',index=0)