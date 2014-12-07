from PIL import Image

def _bellabook(im):
    im = im.convert("P")
    im2 = Image.new("P", im.size,255)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x,y))
            if pix < 50:
                im2.putpixel((x,y),0)

    return im2


def _easyphp(im):
    im = im.convert("P")
    im2 = Image.new("P", im.size,255)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x,y))
            if pix == 215:
                im2.putpixel((x,y),0)

    return im2

def _phpfox(im):
    im = im.convert("P")
    im2 = Image.new("P", im.size,255)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x,y))
            if pix < 200:
                im2.putpixel((x,y),0)

    return im2


def _phpld(im):
    im = im.convert("P")
    im2 = Image.new("P", im.size,255)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x,y))
            if pix < 100:
                im2.putpixel((x,y),0)

    return im2


def _ricar(im):
    im = im.convert("P")
    im2 = Image.new("P", im.size,255)

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            temp[pix] = pix

        if mylist[2]== 1 or mylist[0]==174:
            if pix==mylist[3]:
                im2.putpixel((y,x),0)
        else:
            if pix==mylist[3] or pix==mylist[2]:
                im2.putpixel((y,x),0)
    return im2

def _tikiwiki(im):
    im = im.convert("P")
    im2 = Image.new("P", im.size,255)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x,y))
            if pix < 10:
                im2.putpixel((x,y),0)

    return im2

def _evood(im):
    im=im.convert("P")
    im2 =Image.new("P", im.size,255)

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))

            if pix==0 or pix<100:
                im2.putpixel((y,x),0)
    return im2

def process_image(im):
    width = im.size[0]
    height = im.size[1]

    if width == 110 and height == 35:
        return _bellabook(im)
    elif width == 55 and height == 20:
        return _easyphp(im)
    elif width == 128 and height == 40:
        return _phpfox(im)
    elif width == 125 and height == 30:
        return _phpld(im)
    elif width == 100 and height == 30:
        return _ricar(im)
    elif width == 95 and height == 30:
        return _tikiwiki(im)
    elif width == 142 and height == 52:
        return _evood(im)
    else:
        return im

