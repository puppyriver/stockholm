import sqlite3
import os
import shutil


class QuotaStorage :
    root = 'dbs'
    def __init__(self):
        if not (os.path.exists(self.root)):
            os.mkdir(self.root)
    def insert(self,dayInfo):
        conn = sqlite3.connect(os.path.join(self.root,'%s.db') % dayInfo.code)
        conn.execute('''CREATE TABLE IF NOT EXISTS DAY_INFO 
                        (ID bitint PRIMARY KEY, code varchar,day bigint,high float,low float,
                          volume bigint,open float ,close float,rate float,no bigint,
                          tag1 varchar,tag2 varchar,tag3 varchar )''')
        # cursor = conn.cursor()
        # cursor.execute('CREATE TABLE user (id VARCHAR(20) PRIMARY KEY, name VARCHAR(20))')
        # cursor.close()



        conn.execute("INSERT INTO DAY_INFO (CODE,DAY,NO,OPEN,CLOSE,HIGH,LOW,VOLUME,RATE) VALUES (?,?,?,?,?,?,?,?,?)",
                     (dayInfo.code,dayInfo.day,dayInfo.no,dayInfo.open,dayInfo.close,dayInfo.high,dayInfo.low,dayInfo.volume,dayInfo.rate))
        conn.commit()
        conn.close()

    def insert_many(self,code,dayInfos):
        conn = sqlite3.connect(os.path.join(self.root, '%s.db') % code)
        conn.execute('''CREATE TABLE IF NOT EXISTS DAY_INFO 
                               (ID bitint PRIMARY KEY, code varchar,day bigint,high float,low float,
                                 volume bigint,open float ,close float,rate float,no bigint,
                                 tag1 varchar,tag2 varchar,tag3 varchar )''')
        # cursor = conn.cursor()
        # cursor.execute('CREATE TABLE user (id VARCHAR(20) PRIMARY KEY, name VARCHAR(20))')
        # cursor.close()



        conn.executemany("INSERT INTO DAY_INFO (CODE,NO,DAY,OPEN,CLOSE,HIGH,LOW,VOLUME,RATE) VALUES (?,?,?,?,?,?,?,?,?)",
                     map(lambda dayInfo:(dayInfo.code,dayInfo.no,dayInfo.day,dayInfo.open,dayInfo.close,dayInfo.high,dayInfo.low,dayInfo.volume,dayInfo.rate),dayInfos)                         )
        conn.commit()
        conn.close()


