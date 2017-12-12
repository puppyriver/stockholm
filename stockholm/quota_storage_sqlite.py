import sqlite3
import os
import shutil
from day_info import DayInfo


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

    def clear_db(self,code):
        conn = sqlite3.connect(os.path.join(self.root, '%s.db') % code)
        conn.execute("DELETE FROM DAY_INFO")
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

    def query(self,code,start,end):
        if start is None :
            start = 19900101
        if end is None :
            end = 29900101

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        conn = sqlite3.connect(os.path.join(self.root, '%s.db') % code)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM DAY_INFO WHERE DAY >= ? AND DAY <= ? ORDER BY DAY',(start,end))
        rows = cursor.fetchall()
        day_infos = []
        for row in rows:
            di = DayInfo(row["code"], row["day"], row["open"], row["close"], row["low"], row["high"],round(float( row["close"]) / (float(row["rate"])/100+1),2),
                    row["volume"])
            di.rate = row["rate"]
            day_infos.append(di)
        cursor.close()


        conn.close()
        return day_infos

if __name__ == '__main__':
    QuotaStorage().query("sh600600",20170901,20170904)

