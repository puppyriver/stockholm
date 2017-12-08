class DayInfo :
    def __init__(self,code,open,close,low,high,rate,volume):
        self.code = code
        self.low = low
        self.open = open
        self.close = close
        self.high = high
        self.volume = volume
        self.rate = rate
        self.no = code[1:]


