class DayInfo :
    def __init__(self,code,day,open,close,low,high,pre_close,volume):
        self.day = day
        self.code = code
        self.low = low
        self.open = open
        self.close = close
        self.high = high
        self.volume = volume
        self.pre_close = pre_close
        self.rate = round(100 * (close - pre_close) / pre_close,2)
        self.no = code[1:]


