#-------------------------------------------------------------------------------
# Name:        googlescraper
# Purpose:
#
# Author:      Jangedoo
#
# Created:     21/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from datetime import datetime
import ConnectionManager
import requests
import urlparse
import re
import time
import os
import threading

class GoogleScraper:
    '''
    Class for scraping search results from Google
    '''
    lock = threading.Lock()

    def __init__(self, connectionManager, keywords, event, keywordsFile=None, numberOfPages = 1, googleUrl='http://www.google.com/', thread_count = 4, saveToFile = None):
        '''initializes the class with required parameters'''
        self.connectionManager = connectionManager
        if keywordsFile:
            self.keywords=self._loadKeywords(keywordFile)
        else:
            self.keywords = keywords.split(',')
        self.numberOfPages = numberOfPages
        self.googleUrl = googleUrl
        self.abort = False
        self.event = event
        self.saveToFile = saveToFile

        if thread_count > len(self.keywords): thread_count = len(self.keywords)
        self.thread_count = thread_count


    def _loadKeywords(self, urlFile):
        with open(urlFile, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.keywords.append(line)

    def pop_queue(self):
        keyword = None
        self.lock.acquire()
        if self.keywords:
            keyword = self.keywords.pop()
        self.lock.release()
        return keyword

    def dequeue(self):
        while True:
            keyword = self.pop_queue()
            if not keyword:
                return None

            urls = self.search(keyword)
            if len(urls) == 0:
                print "GOOGLESCRAPER: No results were scraped for keyword {0}.".format(keyword)
                continue

            #trim the keyword by upto 10 chars and then replace any non alphanumeric chars with nothing
            keyword = re.sub('[^\d|\w]','',keyword[:10])
            #save file
            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile
            else:
                if not os.path.exists('./googlescraperresults'):
                    os.mkdir('./googlescraperresults')
                fileName = "./googlescraperresults/{0}_{1}.txt".format(keyword, time.time())
            print "GOOGLESCRAPER: Saving urls for keyword [{0}] to file {1}".format(keyword, fileName)
            try:
                with open(fileName, 'a') as f:
                    for result in urls:
                        print>>f,result
                print "GOOGLESCRAPER: Urls for keyword [{0}] saved to file {1}".format(keyword, os.path.abspath(fileName))
            except Exception,e :
                print "GOOGLESCRAPER: Error while saving urls for keyword [{0}] to file {1}".format(keyword, os.path.abspath(fileName))
                print e

    def start(self):
        #self.event.onStart()
        print "GOOGLESCRAPER: Google scraping started for {0} keywords at {1}".format(len(self.keywords), datetime.now())
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)
        [t.join() for t in threads]
        print "GOOGLESCRAPER: Google scraping completed at {0}".format(datetime.now())
        #self.event.onStop()

    def stop(self):
        self.abort = True

    def search(self, keyword):
        keyword = keyword.strip()
        req = self.connectionManager.getSessionObject()

        print "GOOGLESCRAPER: Scraping started for keyword[{0}], using proxy {1} at {2}".format(keyword, req.proxies['http'], datetime.now())

        searchUrl = self.googleUrl + "search?q={0}&hl=en&output=search&num=10&start=0".format(keyword)
        finalUrls = []
        for pageNumber in range(self.numberOfPages):
            try:
                print "GOOGLESCRAPER: Downloading SERP page {0} for keyword [{1}]".format(pageNumber, keyword)
                resp = req.get(searchUrl)
                soup = BeautifulSoup(resp.text)
                results = soup.findAll('li',{'class':'g'})
                if len(results) == 0:
                    print "GOOGLESCRAPER: No search results found. Aborting..."
                    break

                links = []
                for r in results:
                    url = r.find('a')
                    url = url['href']
                    links.append(url)

                for u in links:
                    match = re.match(r'/url\?q=(http[^&]+)&',u)
                    if match:
                    	finalUrls.append(match.group(1))

                nextSpan = soup.find('span',text='Next')
                if nextSpan:
                    searchUrl = urlparse.urljoin(resp.url, nextSpan.findParent('a').get('href'))
                else:
                    print "GOOGLESCRAPER: Reached end of search results"
                    break
            except Exception, e:
                print "GOOGLESCRAPER: Error while downloading page", e
        return finalUrls


#g = GoogleScraper(ConnectionManager.ConnectionManager(None,None),keywords='site:facebook.com inurl:pages "blackhat seo"',event=None)
#g.start()