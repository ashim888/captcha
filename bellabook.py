import requests
from bs4 import BeautifulSoup
import re
from urlparse import urljoin
from PIL import Image
import cStringIO

import predict
import time

def bellabook(sessionObject, responseObject, dataManager):
        """SessionObject that was used to download the page and ResponseObject that was received from the server"""
        s = sessionObject
        resp = responseObject

        print "Commenting on ", resp.url

        try:

            #Create a request that will persist cookies across the requests

            soup = BeautifulSoup(resp.text)

            #Find the "name" input first
            nameInput = soup.find('input',{'name':'name'})

            #Find the form of the name input
            form = nameInput.findParent('form')


            requestData = {}
            #Find all the inputs in the form and prepare the dictionary
            for i in form.findAll():
                    inputName = i.get('name')

                    if inputName == 'name':
                            requestData['name'] = dataManager.getValue('name')
                    elif inputName == 'email':
                            requestData['email'] = dataManager.getValue('email')
                    elif inputName == 'comments':
                            requestData['comments'] = dataManager.getValue('comment')
                    elif inputName == 'url':
                            requestData['url'] = dataManager.getValue('website')
                    elif inputName == 'captcha':
                            img = form.find('img',{'src':'captcha.php'})
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
                            requestData['captcha'] = captchaText
                    else:
                            if not i.get('value') == None:
                                    requestData[inputName] = i.get('value')

            #Get the abolute url of form handler
            actionUrl = urljoin(resp.url,form.get('action'))
            resp = s.post(actionUrl, data=requestData)

            if "One of the words in your entry is in the bad word list" in resp.text:
                return "Failed to post to "+ resp.url+ " because one of the words in your entry is in the bad word list"
            if "The text you entered didn't match the image, please try again" in resp.text:
                return "Failed to post to "+ resp.url+ " because the captcha text didnot match"
            if "Thank you for signing the guestbook" in resp.text:
                return "Successfully posted to "+ resp.url
            if "The text you entered didn't match the image" in resp.text:
                return "Captcha text was not correct"
            if "Moderation is enabled" in resp.text:
                return "Comment in moderation"
            if "Please fill in your location" in resp.text:
                return "Location not filled"
            else:
                return "Message posted but could not verify. "+ resp.url
        except:
            return "Failed to post to "+ resp.url


