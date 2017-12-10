import requests
import json
import datetime
import timeit
import time
import io
import os
import csv
import re
# from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from quota_agent import  QuotaAgent
from quota_storage_sqlite import QuotaStorage
class QuotaManager(object):

    def __init__(self, agent,storage):
        self.all_quotes_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
        self.index_array = ['000001.SS', '399001.SZ', '000300.SS']
        self.sh000001 = {'Symbol': '000001.SS', 'Name': '上证指数'}
        self.sz399001 = {'Symbol': '399001.SZ', 'Name': '深证成指'}
        self.sh000300 = {'Symbol': '000300.SS', 'Name': '沪深300'}
        self.agent = agent
        self.storage = storage

    def load_history(self,start,end):
        symbols = self.load_all_quote_symbol()
        for symbol in symbols:
            code = symbol['Symbol']
            if code.endswith("SS"):
                code = "sh"+code[:6]
            if code.endswith("SZ"):
                code = "sz"+code[:6]
            history = self.agent.fetchHistory(code, start, end)
            if history is not None:
                self.storage.insert_many(code,history)
                print("%s saved %i records" % (code,len(history)))

    def load_all_quote_symbol(self):
        print("load_all_quote_symbol start..." + "\n")

        start = timeit.default_timer()

        all_quotes = []

        all_quotes.append(self.sh000001)
        all_quotes.append(self.sz399001)
        all_quotes.append(self.sh000300)
        ## all_quotes.append(self.sz399005)
        ## all_quotes.append(self.sz399006)

        try:
            count = 1
            while (count < 100):
                para_val = '[["hq","hs_a","",0,' + str(count) + ',500]]'
                r_params = {'__s': para_val}
                r = requests.get(self.all_quotes_url, params=r_params)
                if (len(r.json()[0]['items']) == 0):
                    break
                for item in r.json()[0]['items']:
                    quote = {}
                    code = item[0]
                    name = item[2]
                    ## convert quote code
                    if (code.find('sh') > -1):
                        code = code[2:] + '.SS'
                    elif (code.find('sz') > -1):
                        code = code[2:] + '.SZ'
                    ## convert quote code end
                    quote['Symbol'] = code
                    quote['Name'] = name
                    all_quotes.append(quote)
                count += 1
        except Exception as e:
            print("Error: Failed to load all stock symbol..." + "\n")
            print(e)

        print("load_all_quote_symbol end... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
        return all_quotes


if __name__ == '__main__':
    qm = QuotaManager(QuotaAgent(),QuotaStorage())
    t1 = time.time();
    qm.load_history(19900101,20171212)
    print("spend "+str(time.time()-t1)+" seconds")