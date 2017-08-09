import sys, os, re
from PIL import Image

while(1):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    x = input()
    dir_path += x
    print (dir_path)
    allList_back = os.listdir(dir_path)
    all_pictures = []
    # Setting the regular expression to only look for .jpg extenstion
    jpgRE = re.compile('^\w+.jpg$', re.I)
    # Removing any files that do not have an .fbx extenstion
    for fname in allList_back:
        bk = jpgRE.search(fname)
        if bk:
            all_pictures.append(fname)
    images = map(Image.open, all_pictures)
    widths, heights = zip(*(i.size for i in images))

    total_width = max(widths)*4
    max_height = max(heights)*3

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    y_offset = 0
    n = 0
    for im in images:
        new_im.paste(im, (x_offset,y_offset))
        n += 1
        if n % 4 == 0:
            x_offset = 0
            y_offset += im.size[1]
        else:
            x_offset += im.size[0]
      print(im.format, im.size, im.mode)

    new_im.save('toal.jpg')
