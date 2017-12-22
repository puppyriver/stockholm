import imghdr
import os

for file in os.walk("download_images"):
    if imghdr.what(file):
        # good image
        pass
    else:
        # bad image
        print("invalid image %s" % file)

