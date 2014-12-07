from PIL import Image

def segment_image(im):

    segments = []
    inletter = False
    foundletter = False
    start = 0
    end = 0
    #Vertical segmentation
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pix = im.getpixel((x,y))
            if pix != 255:
                inletter = True

        if foundletter == False and inletter == True:
            foundletter = True
            start = x

        if foundletter == True and inletter == False:
            foundletter = False
            end = x
            im2 = im.crop((start,0,end, im.size[1]))
            #horizontal segmentation
            inletter1 = False
            foundletter1 = False
            start1 = 0
            end1= 0

            for y1 in range(im2.size[1]):
                for x1 in range(im2.size[0]):
                    pix = im2.getpixel((x1,y1))
                    if pix != 255:
                        inletter1 = True
                if foundletter1 == False and inletter1 ==True:
                    foundletter1 = True
                    start1 = y1

                if foundletter1 == True and inletter1 == False:
                    foundletter1 = False
                    end1 = y1
                    im3 = im2.crop((0,start1,im2.size[0], end1))
                    if im3.size[1]> 8:
                        im4 = im3.resize((25,25))
                        segments.append(im4)
                inletter1 = False
        inletter = False

    return segments
