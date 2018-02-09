# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 14:52:17 2018

@author: RASHMI
"""
import sys
import numpy as np
import os
from six.moves import urllib
import pandas as pd
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
count = 0

#Function that returns the strongest retailer affinity relative to other brands    
def retailer_affinity(focus_brand):
    global df
    global count
    a = df[df['Parent Brand'] == focus_brand]
    grouped_data = a.groupby('Retailer')
    sum_per_retailer = grouped_data['Item Units'].agg(np.sum)
    print(sum_per_retailer)


    my_dict = {}
    j =0
    for i in grouped_data:
        my_dict[i[0]]=sum_per_retailer[j]
        j = j+1
    maximum = max(my_dict, key=my_dict.get)
    print("The Maximum items sold by Retailer for ",focus_brand +" is "+ maximum, my_dict[maximum])
    
    b = df[df['Retailer'] == maximum]
    grouped_brand = b.groupby('Parent Brand')
    sum_per_brand = grouped_brand['Item Units'].agg(np.sum)
    print(sum_per_brand)
    plt.figure(figsize = (17,7))
    plt.subplot(1,2,1)
    
    sum_per_retailer.plot(kind ='bar')
    plt.xlabel("Retailers")
    plt.ylabel("No of Items")
    plt.title("Items sold by each retailer for " + focus_brand)
    plt.subplot(1,2,2)
    sum_per_brand.plot(kind ='bar')
    plt.xlabel("Brands")
    plt.ylabel("No of Items")
    plt.title("Count of items belonging to different brand sold by the " + maximum)
    plt.show(block = False)
    time.sleep(15)
    plt.close()
    my_dict1 = {}
    j =0
    for i in grouped_brand:
        my_dict1[i[0]]=sum_per_brand[j]
        j = j+1
    maximum1 = max(my_dict1, key=my_dict1.get)
    print("The brand with top retailer is: \n",maximum1, my_dict1[maximum1])
    
    
    if my_dict1[maximum1] == my_dict[maximum]:
        print("THE STRONGEST AFFINITY RETAILER REALTIVE TO OTHER BRANDS IS :",maximum)

    else:
        count = count + 1
        df = df[df.Retailer != maximum]
        if count == 8:
            print("NO STRONG RETAILER AFFINITY FOUND")
        else:
            retailer_affinity(focus_brand)
    
    
if __name__ == '__main__':
    focus_brand = str(sys.argv[1])
    retailer_affinity(focus_brand)
    
