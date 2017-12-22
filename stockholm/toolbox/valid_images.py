import imghdr
import os

for parent, dirnames, filenames  in os.walk("download_images"):
    for image in filenames:
        file = os.path.join(parent,image)
        if imghdr.what(file):
            # good image
            pass
        else:
            # bad image
            print("invalid image %s" % file)


