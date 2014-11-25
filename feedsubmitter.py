import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import ConnectionManager
import urllib
class FeedSubmitter:
    def __init__(self, proxyFile, userUrls, **kwargs):
        self.connectionManager = ConnectionManager.ConnectionManager(proxyFile)
        self.userUrls = userUrls
        self.icerocketUrl = r'http://www.icerocket.com/c?p=ping&url='
        self.goldenfeedUrl = r'http://www.goldenfeed.com/AddFeed.aspx'
        self.feedgyUrl = r'http://feedgy.com/Submit.aspx'
        self.readablogUrl = r'http://www.readablog.com/rss-submit/'
        self.plazooUrl = r'http://www.plazoo.com/en/addrss.asp'
        self.blogdiggerUrl = r'http://blogdigger.com/add.jsp'
        self.xmetaUrl = r'http://www.xmeta.net/users/'
        self.urlfanxUrl = r'http://www.urlfanx.com/search_not_found.php3?no_cache=1'
        self.args = kwargs


    def submit(self, iceRocket=True, feedGy=True, readaBlog=True, plazoo=True, blogDigger=True, xmeta=True, urlfanx=True):
        pass

    def submitIcerocket(self):
        for url in self.userUrls:
            req = self.connectionManager.getSessionObject()
            try:
                resp = req.get(self.icerocketUrl + urllib.urlencode(url))
                print "Submitted to IceRocket successfully"
            except:
                print "Error occured while submitting to IceRocket."

    def submitGoldenfeed(self):
        for url in self.userUrls:
            req = self.connectionManager.getSessionObject()
            try:
                resp = req.get(self.goldenfeedUrl)
                soup = BeautifulSoup(resp.text)
                requestData = {}
                form = soup.find('form',attrs={'action':'AddFeed.aspx'})
                for input in form.find('input'):
                    inputName = str(i.get('name'))

                    if "RSSURL" in inputName:
                        requestData[inputName] = url
                    else:
                        if not i.get('value') == None:
                            requestData[inputName] = i.get('value')

                #Get absolute url of form
                actionUrl = urljoin(resp.url, form.get('action'))
                resp = req.post(actionUrl, data=requestData)
                print "Submitted to GoldenFeed succesfully"
            except:
                print "Error occured while submitting to GoldenFeed"

    '''
    http://www.readablog.com/rss-submit/
    form anction=http://www.readablog.com/rss-submit/
    input name = email
    input name = url
    input name = code
    img src = /files/inc.captcha.php
    Please enter the Security Code as displayed
    Please enter a valid RSS Feed that starts with http://, https:// or feed://
    Sorry, the submitted blog feed does not seem to be in a valid XML format!
    Your submission has been received, thank you.
    '''
    def submitReadablog(self):
        for url in self.userUrls:
            req = self.connectionManager.getSessionObject()
            try:
                resp = req.get(self.readablogUrl)
                soup = BeautifulSoup(resp.text)
                requestData = {}
                form = soup.find('form',attrs={'action':'http://www.readablog.com/rss-submit'})
                for input in form.find('input'):
                    inputName = input.get('name')
                    if inputName == "email":
                        requestData[inputName] = self.args['email']
                    elif inputName == "url":
                        requestData[inputName] = url
                    elif inputName == "code":
                        img = form.find('img',{'src':'/files/inc.captcha.php'})
                        imgUrl = img.get('src')
                        imgUrl = urljoin(resp.url, imgUrl)

                        #Download Image
                        r = req.get(imgUrl)
                        file_like = cStringIO.StringIO(r.content)
                        im = Image.open(file_like)
                        captchaText = predict.predict(im)
                        requestData[inputName] = captchaText
                    else:
                        if not i.get('value') == None:
                            requestData[inputName] = i.get('value')
                actionUrl = urljoin(resp.url, form.get('action'))
                resp = s.post(actionUrl, data=requestData)

                if "Please enter the Security Code as displayed" in resp.text:
                    print "Submission failed. Captcha code was not correct"
                elif "Please enter a valid RSS Feed" in resp.text:
                    print "Submission failed. Not a valid RSS feed"
                elif "the submitted blog feed does not seem to be in a valid XML format" in resp.text:
                    print "Submission failed. Blog feed not in valid XML format"
                elif "submission has been received" in resp.text:
                    print "Submitted to ReadABlog"