# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 14:13:31 2018

@author: RASHMI
"""

import pandas as pd
import numpy as np
import os
from six.moves import urllib
import matplotlib.pyplot as plt
import time

#Downloading the file from source
DOWNLOAD_ROOT = "https://s3.amazonaws.com/"
INFO_PATH = "isc-isc"
INFO_URL = DOWNLOAD_ROOT + INFO_PATH + "/trips_gdrive.csv"

def fetch_info_data(info_url=INFO_URL,info_path=INFO_PATH):
    if not os.path.isdir(info_path):
        os.makedirs(info_path)
    file_path = os.path.join(info_path, "trips_gdrive.csv")
    urllib.request.urlretrieve(info_url,file_path)
    
fetch_info_data()

#Reading the downloaded file
def load_info_data(info_path=INFO_PATH):
    csv_path = os.path.join(info_path, "trips_gdrive.csv")
    return pd.read_csv(csv_path)

#Passing the file to a dataframe
df  = load_info_data()

def top_buying_brand():
    global df
    df['currency'],df['dollars'] = df['Item Dollars'].str.split('$', 1).str
    df = df.drop('currency', axis = 1)
    df['dollars'] = df['dollars'].astype(int)
    df['Transaction_amt'] = (df['dollars'] * df['Item Units'])
    grouped = df.groupby('Parent Brand')
    sum_per_brand = grouped['Transaction_amt'].agg(np.sum)
    no_of_HH = grouped['User ID'].nunique()
    rate = sum_per_brand/no_of_HH
    data = pd.DataFrame(rate,columns = ['Buying Rate'])
    data.style.format('${:,.4f}')
    data.plot(kind = 'bar')
    plt.show(block = False)
    time.sleep(5)
    plt.close()
    my_dict = {}
    j =0
    for i in grouped:
        my_dict[i[0]]=rate[j]
        j = j+1
    maximum = max(my_dict, key=my_dict.get)  
    print("The Parent brand with top buying rate is: \n",maximum, my_dict[maximum])

if __name__ == '__main__':
    top_buying_brand()
