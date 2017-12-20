import urllib.request
import os
import os.path

get_all_sub_id_url = "http://image-net.org/api/text/wordnet.structure.hyponym?wnid=%s&full=1"
get_image_url_url = "http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=%s"

def get_all_sub_ids(parentId):
    sub_ids = []
    f = urllib.request.urlopen(get_all_sub_id_url % parentId)
    data = f.readlines()
    for l in data:
        line = str(l, "utf-8").strip()
        if (line.startswith("-")):
            sub_ids.append(line[1:])
    return sub_ids

def download_images(wnid,word):
    print("--------------------------- %s :: %s " % (wnid,word))
    image_urls = []
    f = urllib.request.urlopen(get_image_url_url % wnid)
    data = f.readlines()
    for l in data:
        line = str(l, "utf-8").strip()
        image_urls.append(line)

    image_root_dir = 'download_images'
    if not (os.path.exists(image_root_dir)):
        os.mkdir(image_root_dir)

    dir = os.path.join(image_root_dir, word)
    if not (os.path.exists(dir)):
        os.mkdir(dir)

    for image_url in image_urls:
        try:
            file_name = image_url[image_url.rindex("/") + 1:]
            print('%s save to %s' % (image_url, file_name))
            urllib.request.urlretrieve(image_url, os.path.join(dir, file_name))
        except Exception as e:
            print(e)
            pass


# aa = get_all_sub_ids("n07881800")

words = open('words.txt')
root_wnid = ""
id_word = {}
for line in words:
    kv = line.split("\t")
    # print("k=%s v=%s" % (kv[0],kv[1]))
    id_word[kv[0]] = kv[1].strip()


sub_ids = get_all_sub_ids("n07881800")
print("sub_ids length = %i",len(sub_ids))
for sub_id in sub_ids:
    word = id_word[sub_id]
    try:
        download_images(sub_id,word)
    except Exception as e:
        print("error download : %s %s" % (sub_id,word),e)

