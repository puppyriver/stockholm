import requests
from day_info import  DayInfo
class QuotaAgent :
    real_time_url = "http://hq.sinajs.cn"
    history_url = "http://q.stock.sohu.com/hisHq"
    def fetchDayInfo(self,code):
        r_params = {'list': code}
        r = requests.get(self.real_time_url, params=r_params)
        if (r.status_code == 200):
            print(r.text)
            text = r.text
            text = text[ text.index("\"")+1:text.rindex("\"")]
            values = text.split(",")
            yesterday = float(values[2]);
            now = float(values[3])
            rate = 100 * (now - yesterday) / yesterday
            day_info = DayInfo(code,float(values[1]),now,float(values[5]),float(values[4]),rate,int(values[8]))
            # print(r.json())

    def fetchHistory(self,code,start,end):
        r_params = {'code' : code,'start': start,'end':end,'stat':1,'order':'D','period':'d','rt':'jsonp'}
        r = requests.get(self.history_url, params=r_params)



if __name__ == '__main__':
    qa = QuotaAgent()
    qa.fetchDayInfo("sh600600")