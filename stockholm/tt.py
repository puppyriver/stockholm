from day_info import DayInfo
import time
import threadpool


def rnb(k):
    print("running %i" , k)
    time.sleep(3)
    return k;

def cb(req,k):
    print("callback:")
    print(k)

pool = threadpool.ThreadPool(5)
requests = []
for i in range(10):
    requests.extend(threadpool.makeRequests(rnb, [((i,), {})],cb))

[pool.putRequest(req) for req in requests]
# map(pool.putRequest, requests)
p = pool.poll()
print(p)
