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
        notImg = False
        if imghdr.what(file):
            size = os.path.getsize(file)
            if size == 2051 or size < 1000:
                notImg = True

        else:
            with open(file, "rb") as f:
                bytes = f.read()
                if not (bytes.startswith(b'\xff\xd8') or bytes.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')):
                    # bad image
                    print("invalid image %s" % file)
                    notImg = True


        if notImg:
            shutil.move(file, os.path.join(invalid_dest, image))

        else:
            if not (image.find(".") > 0):
                shutil.move(file, os.path.join(parent,image+".jpg"))
                print("change file name %s to %s" % (image,image+".jpg"))



