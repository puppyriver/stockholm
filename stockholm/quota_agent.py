import requests
class QuotaAgent :
    url = "http://hq.sinajs.cn"
    def fetchDayInfo(self,code):
        r_params = {'list': code}
        r = requests.get(self.url, params=r_params)
        print(r.json())


if __name__ == '__main__':
    qa = QuotaAgent()
    qa.fetchDayInfo("sh600600")