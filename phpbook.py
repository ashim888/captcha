import requests
from bs4 import BeautifulSoup
import re
from urlparse import urljoin
from PIL import Image
import cStringIO

import predict
import time

def phpbook(sessionObject, responseObject, dataManager):
        """SessionObject that was used to download the page and ResponseObject that was received from the server"""
        s = sessionObject
        resp = responseObject

        location = ['America','Britain','Brazil','NewZealand','Australia','Sweden','Nepal','Argentina','Syprus','Holland','Spain','Greece','Russia','China','Korea']
        print "Commenting on ", resp.url

        try:

            #Create a request that will persist cookies across the requests

            soup = BeautifulSoup(resp.text)

            #Find the "name" input first
            nameInput = soup.find('input',{'name':'in[name]'})

            #Find the form of the name input
            form = nameInput.findParent('form')


            requestData = {}
            #Find all the inputs in the form and prepare the dictionary
            for i in form.findAll():
                    inputName = i.get('name')

                    if inputName == 'in[name]':
                            requestData['in[name]'] = dataManager.getValue('name')
                    elif inputName == 'in[email]':
                            requestData['in[email]'] = dataManager.getValue('email')
                    elif inputName == 'in[message]':
                            requestData['in[message]'] = dataManager.getValue('comment')
                    elif inputName == 'in[http]':
                            requestData['in[http]'] = dataManager.getValue('website')
                    elif inputName == 'in[location]':
                            requestData['in[location]'] = random.choice(location)
                    elif inputName == 'in[confirm_code]':
                            imgs = form.findAll('img')
                            for i in imgs:
                                if 'confirm_image.php?random_num' in i.get('src'):
                                    imgUrl = i.get('src')

                            if not imgUrl: raise "Error while downloading captcha image"
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
                            requestData['in[confirm_code]'] = captchaText
                    else:
                            if not i.get('value') == None:
                                    requestData[inputName] = i.get('value')

            #Get the abolute url of form handler
            actionUrl = urljoin(resp.url,form.get('action'))
            resp = s.post(actionUrl, data=requestData)

            return "Posted to " + resp.url
        except:
            return "Failed to post to " + resp.url


