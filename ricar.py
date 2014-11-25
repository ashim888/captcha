import requests
from bs4 import BeautifulSoup
import re
from urlparse import urljoin
from PIL import Image
import cStringIO

import predict
import time

def ricar(sessionObject, responseObject, dataManager):
        """SessionObject that was used to download the page and ResponseObject that was received from the server"""
        s = sessionObject
        resp = responseObject

        location = ['America','Britain','Brazil','NewZealand','Australia','Sweden','Nepal','Argentina','Syprus','Holland','Spain','Greece','Russia','China','Korea']
        print "Commenting on ", resp.url

        try:

            #Create a request that will persist cookies across the requests

            soup = BeautifulSoup(resp.text)

            #Find the "name" input first
            nameInput = soup.find('input',{'name':'nick'})

            #Find the form of the name input
            form = nameInput.findParent('form')


            requestData = {}
            #Find all the inputs in the form and prepare the dictionary
            for i in form.findAll():
                    inputName = i.get('name')

                    if inputName == 'nick':
                            requestData['nick'] = dataManager.getValue('name')
                    elif inputName == 'email':
                            requestData['email'] = dataManager.getValue('email')
                    elif inputName == 'comment':
                            requestData['comment'] = dataManager.getValue('comment')
                    elif inputName == 'web':
                            requestData['web'] = dataManager.getValue('website')
                    elif inputName == 'location':
                            requestData['location'] = random.choice(location)
                    elif inputName == 'seccode':
                            img = form.find('img',{'src':'image.php'})
                            imgUrl = img.get('src')
                            #make imgUrl absolute
                            imgUrl = urljoin(resp.url, imgUrl)

                            #Download the image
                            r = s.get(imgUrl)
                            #PIL accepts file-like objects or file name
                            #So creake a file-like object from the image content
                            file_like = cStringIO.StringIO(r.content)
                            im = Image.open(file_like)
                            captchaText = predict.predict(im)
                            print captchaText
                            requestData['seccode'] = captchaText
                    else:
                            if not i.get('value') == None:
                                    requestData[inputName] = i.get('value')

            #Get the abolute url of form handler
            actionUrl = urljoin(resp.url,form.get('action'))
            resp = s.post(actionUrl, data=requestData)

            return "Posted to " + resp.url
        except:
            return "Failed to post to " + resp.url


