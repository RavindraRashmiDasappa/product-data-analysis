# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 13:32:33 2018

@author: RASHMI
"""
import pandas as pd
import argparse
import os
from six.moves import urllib

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


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-b", "--brand", help="Brand.", type=str, default=None)
    parser.add_argument("-r", "--retailer", help="retailer.", type=str, default=None)
    parser.add_argument("-sd", "--start_date", help="Start date.", type=str, default=None)
    parser.add_argument("-ed", "--end_date", help="end date.", type=str, default=None)

    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')

    # Parse arguments
    args = parser.parse_args()

    return args

def count_hhs(brand, retailer, start_date, end_date):
    global df
    a = df
    result = []
    if(brand != None):
        a = df[df['Parent Brand'] == brand]
        result.append(a['User ID'].nunique())
    if (retailer != None):
        a = a[a['Retailer'] == retailer]
        result.append(a['User ID'].nunique())
    if (start_date != None):
        a['Date'] = pd.to_datetime(a['Date'])
        df_sorted = a.sort_values(by=['Date'])
        a = df_sorted[df_sorted['Date'] >= start_date]
        result.append(a['User ID'].nunique())
    if (end_date != None):
        a['Date'] = pd.to_datetime(a['Date'])
        df_sorted = a.sort_values(by=['Date'])
        a = df_sorted[df_sorted['Date'] <= end_date]
        result.append(a['User ID'].nunique())
    else:
        result.append(a['User ID'].nunique())
        
    for i in range(len(result)):
        if i == len(result)-1:
            print("THE NUMBER OF HOUSEHOLDS FOR THE GIVEN ARGUMENTS IS ",result[i])
            break
        else:
            continue

if __name__ == '__main__':
    args = parseArguments()

    # Raw print arguments
    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))
    count_hhs(args.brand, args.retailer, args.start_date, args.end_date)
