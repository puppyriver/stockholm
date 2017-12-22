import imghdr
import os
import shutil

# type = imghdr.what("bb.jpg")

invalid_dest = "invalid_images"
if not os.path.exists(invalid_dest):
    os.mkdir(invalid_dest)

for parent, dirnames, filenames  in os.walk("download_images"):
    for image in filenames:
        file = os.path.join(parent,image)
        if imghdr.what(file):
            # good image
            pass
        else:
            with open(file, "rb") as f:
                bytes = f.read()
                if not (bytes.startswith(b'\xff\xd8')):
                    # bad image
                    print("invalid image %s" % file)
                    shutil.copy(file, os.path.join(invalid_dest, image))



