from PIL import Image
import os
import math
import time
import segmenter
import preprocessor
import pickle

class VectorCompare:
  def magnitude(self,concordance):
    total = 0
    for word,count in concordance.iteritems():
      total += count ** 2
    return math.sqrt(total)

  def relation(self,concordance1, concordance2):
    relevance = 0
    topvalue = 0
    for word, count in concordance1.iteritems():
      if concordance2.has_key(word):
        topvalue += count * concordance2[word]
    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))



def buildvector(im):
  d1 = {}

  count = 0
  for i in im.getdata():
    d1[count] = i
    count += 1

  return d1



v = VectorCompare()
imageset = pickle.load(open("./imgdata.data","r"))


def predict(im):
    im = preprocessor.process_image(im)
    segments = segmenter.segment_image(im)
    output = ""
    for i in segments:
        guess = []
        for image in imageset:
            for x,y in image.iteritems():
                if(len(y)!=0):
                    guess.append((v.relation(y[0],buildvector(i)), x))
        guess.sort(reverse=True)
        output += str(guess[0][1])
    return output