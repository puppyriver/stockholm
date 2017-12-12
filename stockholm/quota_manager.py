import requests
import json
import datetime
import timeit
import time
import io
import os
import csv
import re
import argparse
import threadpool
# from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from quota_agent import QuotaAgent
from quota_storage_sqlite import QuotaStorage


class QuotaManager(object):
    def __init__(self, agent, storage):
        self.all_quotes_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
        self.index_array = ['000001.SS', '399001.SZ', '000300.SS']
        self.sh000001 = {'Symbol': '000001.SS', 'Name': '上证指数'}
        self.sz399001 = {'Symbol': '399001.SZ', 'Name': '深证成指'}
        self.sh000300 = {'Symbol': '000300.SS', 'Name': '沪深300'}
        self.agent = agent
        self.storage = storage

    def load_history(self, start, end):
        symbols = self.load_all_quote_symbol()
        for symbol in symbols:
            code = symbol['Symbol']
            if code.endswith("SS"):
                code = "sh" + code[:6]
            if code.endswith("SZ"):
                code = "sz" + code[:6]
            history = self.agent.fetchHistory(code, start, end)
            if history is not None:
                try:
                    db_infos = self.storage.query(code, start, end)
                    if (db_infos is not None and len(db_infos) > 0):
                        history = list(
                            filter(lambda h: list(filter(lambda d: d.day == h.day, db_infos)) == [], history))
                except Exception as e:
                    print('error:', e)
                finally:
                    self.storage.insert_many(code, history)
                    print("%s saved %i records" % (code, len(history)))

    def analyst_now(self):
        nows = self.storage.query("now")
        for now in nows:
            try:
                history = self.storage.query(now.code,20170608,20171231)
                min_volume = min(list(map(lambda n: n.volume, history)))
                min_close = min(list(map(lambda n: n.close, history)))
                if (len(history) > 15):
                    min_close = min(list(map(lambda n: n.close, history))[-10:])

                if len(history) > 10 and min_volume > (now.volume * 2 / 100) and min_close > now.close:
                    print(now.code,min_volume,now.volume/100)
            except Exception as e:
                print("Error load : %s" % now.code,e)

    def load_nows(self):
        symbols = self.load_all_quote_symbol()
        pool = threadpool.ThreadPool(10)

        nows = []

        def do_fetch(_code):
            print("fetching %s..." % _code)
            now = self.agent.fetchDayInfo(_code)
            nows.append(now)
            return now

        request_list = []

        for symbol in symbols:
            code = symbol['Symbol']
            if code.endswith("SS"):
                code = "sh" + code[:6]
            if code.endswith("SZ"):
                code = "sz" + code[:6]
            request_list.extend(threadpool.makeRequests(do_fetch,[((code,),{})],lambda req,result:print(result)))

            # do_fetch(code)
        list(map(pool.putRequest, request_list))
        pool.wait()
        self.storage.clear_db("now")
        self.storage.insert_many("now", nows)
        print("%i saved" % len(nows))
        return nows

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
    qm = QuotaManager(QuotaAgent(), QuotaStorage())

    # qm.load_history(20171201,20171212)



    ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--images", required=True,
    #                 help="path to input directory of images")
    # ap.add_argument("-i", "--images", type=str, default="H:\\mumu_pictures\\camera20171007.0")
    ap.add_argument("-t", "--type", type=str, default="now")
    # ap.add_argument("-t", "--threshold", type=float, default=100.0,
    #                 help="focus measures that fall below this value will be considered 'blurry'")
    args = vars(ap.parse_args())
    if (args["type"] == 'now'):
        t1 = time.time();
        qm.load_nows()
        print("spend " + str(time.time() - t1) + " seconds")
    elif (args["type"] == 'history'):
        while True:
            now = datetime.datetime.now()
            if now.hour == 20 and now.minute < 2:
                t1 = time.time();
                qm.load_history(20171201, 20191230)
                print("spend " + str(time.time() - t1) + " seconds")
            elif now.hour >= 9 and now.hour <= 15:
                qm.load_nows()
            time.sleep(60)
    elif (args["type"] == 'historynow'):
        t1 = time.time();
        qm.load_history(19900101, 20191230)
        print("spend " + str(time.time() - t1) + " seconds")
    elif (args['type'] == 'analyst'):
        qm.analyst_now()
