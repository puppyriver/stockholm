#coding:utf-8
import requests
import json
import datetime
import timeit
import time
import io
import os
import csv
import re
import requests
import urllib.request

if __name__ == '__main__':
    for page in range(1,200):
        url = "https://t66y.com/thread0806.php?fid=25&search=&page="+str(page);
        r = requests.get(url)
        if (r.status_code == 200):
            text = r.text
            text = str(text,"utf-8")
            if text.find("cdmindstorm") > 0:
                print("find cdmindstorm - "+str(page))
            if text.find("rxrj") > 0:
                print("find rxrj :"+str(page));
            else:
                print("not find : "+str(page));

        # f = urllib.request.urlopen(url)
        # data = f.readlines()
        # for l in data:
        #     line = str(l, "utf-8").strip()
        #     if page == 1:
        #         print(line);
        #     if line.find("rxrj") > 0:
        #         print("find rxrj :" + str(page));
        #     else:
        #         print("not find : "+str(page));

