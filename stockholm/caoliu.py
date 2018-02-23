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

if __name__ == '__main__':
    for page in range(1,200):
        r_params = {};
        r = requests.get("https://t66y.com/thread0806.php?fid=25&search=&page="+page)
        if (r.status_code == 200):
            text = r.text
            if text.find("rxrj") > 0:
                print("find rxrj :"+page);
            else:
                print("not find : "+page);  


