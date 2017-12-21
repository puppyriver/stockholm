import urllib.request
import os
import os.path
import socket
import threadpool

pool = threadpool.ThreadPool(15)
socket.setdefaulttimeout(30)

get_all_sub_id_url = "http://image-net.org/api/text/wordnet.structure.hyponym?wnid=%s&full=1"
get_sub_id_url = "http://image-net.org/api/text/wordnet.structure.hyponym?wnid=%s"
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


def get_sub_ids_tree(parentId):
    sub_ids = []
    f = urllib.request.urlopen(get_sub_id_url % parentId)
    data = f.readlines()
    for l in data:
        line = str(l, "utf-8").strip()
        if (line.startswith("-")):
            sub_id = line[1:]
            sub_ids.append(get_sub_ids_tree(sub_id))
    return (parentId, sub_ids)


def download_images(wnid, word, parent=None):
    print("--------------------------- %s :: %s >> %s" % (wnid, word,parent))
    image_urls = []
    f = urllib.request.urlopen(get_image_url_url % wnid)
    data = f.readlines()
    for l in data:
        line = str(l, "utf-8").strip()
        image_urls.append(line)

    image_root_dir = 'download_images'
    if not (os.path.exists(image_root_dir)):
        os.mkdir(image_root_dir)

    parent_dir = image_root_dir
    if parent is not None:
        parent_dir = os.path.join(image_root_dir,parent)

    dir = os.path.join(parent_dir, word)
    if not (os.path.exists(dir)):
        os.makedirs(dir,exist_ok=True)
    else:
        print("%s existed !" % dir)
        return

    for image_url in image_urls:
        try:
            file_name = image_url[image_url.rindex("/") + 1:]
            print('%s save to %s' % (image_url, file_name))
            urllib.request.urlretrieve(image_url, os.path.join(dir, file_name))
        except Exception as e:
            print(e)
            # pass
    return "success: %s %s" % (wnid, word)


# aa = get_all_sub_ids("n07881800")

words = open('words.txt')
root_wnid = ""
id_word = {}
for line in words:
    kv = line.split("\t")
    # print("k=%s v=%s" % (kv[0],kv[1]))
    id_word[kv[0]] = kv[1].strip()

root_node = get_sub_ids_tree("n00021265")
sub_nodes = root_node[1]
print("sub_ids length = %i", len(sub_nodes))


def make_node_task(sub_id, word, parent):
    requests = threadpool.makeRequests(download_images, [((sub_id, word,parent), {})],
                                       lambda req, result: print(result),
                                       lambda req, exp: print("error download : %s %s" % (sub_id, word),
                                                              exp.read().decode("utf-8")))
    [pool.putRequest(req) for req in requests]


def process_node(node,parent = ""):
    node_id = node[0]
    sub_nodes = node[1]
    word = id_word[node_id]
    make_node_task(node_id, parent)
    for sub_node in sub_nodes:
        process_node(sub_node,os.path.join(parent,word))

process_node(root_node)

pool.wait()

print("download successfully !")


# for sub_id in sub_ids:
#     word = id_word[sub_id]
#
#     requests = threadpool.makeRequests(download_images, [((sub_id, word), {})],
#                                        lambda req, result: print(result),
#                                        lambda req, exp: print("error download : %s %s" % (sub_id, word),
#                                                               exp.read().decode("utf-8")))
#     [pool.putRequest(req) for req in requests]
#
# pool.wait()

#
# try:
#     download_images(sub_id,word)
# except Exception as e:
#     print("error download : %s %s" % (sub_id,word),e)
