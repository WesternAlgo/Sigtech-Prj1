
#Imports
from ast import increment_lineno
import warnings

import matplotlib
warnings.filterwarnings('ignore')

import gzip
import shutil
from struct import unpack
from collections import namedtuple, Counter, defaultdict
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urljoin
from datetime import timedelta
from time import time
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

sns.set_style('whitegrid')

#Return formatted time
def format_time(t): 
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return (f'{h}:{m}:{s}')


#Establishing location where data will be stored
data_path = Path('data')
itch_store = str(data_path/'itch.h5')
order_book_store = data_path/'order_book.h5'

#Going to the website shown below, you can choose the exact data you want
FTP_URL = 'https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/'
SOURCE_FILE = '01302019.NASDAQ_ITCH50.gz'

#Downloads and unzip ITCH data if not yet available
def may_be_download(url):
    if not data_path.exists():
        print("Creating dir")
        data_path.mkdir()
    else:
        print("Dir exists")
    
    filename = data_path / url.split('/')[-1]
    
    if not filename.exists():
        print("Downloading...", url)
        urlretrieve(url, filename)
    else:
        print("File exists")
    
    unzipped = data_path / (filename.stem + ".bin")
    if not unzipped.exists():
        print('Unzipping to ', unzipped)
        with gzip.open(str(filename), 'rb') as f_in:
            with open(unzipped, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        print('File already unpacked')
    return unzipped

#Calling methods
file_name = may_be_download(urljoin(FTP_URL, SOURCE_FILE))
date = file_name.name.split('.')[0]