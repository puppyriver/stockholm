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
            pre_close = float(values[2]);
            now = float(values[3])
            # rate = 100 * (now - yesterday) / yesterday
            open = float(values[1])
            low = float(values[5])
            high = float(values[4])
            volume = int(values[8])
            day_no = values[30].replace('-','')
            day_info = DayInfo(code,day_no, open, now, low, high, pre_close, volume)
            print(day_info)
            return day_info
            # print(r.json())
        else:
            print("error:"+r.text)

    def fetchHistory(self,code,start,end):
        r_params = {'code' : "cn_"+code[2:],'start': start,'end':end,'stat':1,'order':'D','period':'d','rt':'jsonp'}
        r = requests.get(self.history_url, params=r_params)
        if (r.status_code == 200):
            text = r.text
            if text.find("[[") < 0 or text.find("]]") < 0:
                print(code+": Error text : "+text)
            else :
                text = text[text.index("[[") :text.rindex("]]")+2]
                days = eval(text)
                history = []
                for day in days:
                    now = float(day[2])
                    pre_close = now / (1 + (float(day[4].strip("%"))/100))
                    pre_close = round(pre_close,2)
                    # rate = 100 * (now - yesterday) / yesterday
                    open = float(day[1])
                    low = float(day[5])
                    high = float(day[6])
                    volume = int(day[7])
                    day_no = int(day[0].replace('-',''))
                    day_info = DayInfo(code,day_no, open, now, low, high, pre_close, volume)
                    history.append(day_info)

                return history


if __name__ == '__main__':
    qa = QuotaAgent()
    qa.fetchDayInfo("sh600600")
    # qa.fetchHistory("sh600600",20171101,20171130)