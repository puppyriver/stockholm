import urllib.request
import os
import os.path

path = 'urls/vegetable.txt'
file_object = open(path)
dir = path[path.rindex("/")+1:path.rindex(".")]
if not (os.path.exists(dir)):
    os.mkdir(dir)

try:
  for line in file_object:
    try:
        line = line.strip()
        file_name = line[line.rindex("/")+1:]
        print('%s save to %s' % (line,file_name))
        urllib.request.urlretrieve(line,os.path.join(dir,file_name))
    except Exception as e:
        print(e)
        pass
finally:
    file_object.close()