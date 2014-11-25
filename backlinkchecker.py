#-------------------------------------------------------------------------------
# Name:        backlinkchecker
# Purpose:
#
# Author:      Jangedoo
#
# Created:     23/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests
import os, sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urlparse import urljoin
import urlparse
import threading
import csv

class BacklinkChecher:
    def __init__(self, urlFile, yoururlFile, connectionManager, event, numberOfThreads=4, saveToFile = None):
        self.urls = self._loadData(urlFile)
        self.yourUrls = self._loadData(yoururlFile)
        self.event = event
        self.numberOfThreads=numberOfThreads
        self.saveToFile = saveToFile
        self.connectionManager = connectionManager
        self.abort = False
        self.lock = threading.Lock()
        self.finalData = {}


    def _loadData(self, fileName):
        lines = []
        with open(fileName, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        return lines

    def pop_queue(self):
        url = None
        self.lock.acquire()
        if self.urls:
            url = self.urls.pop()
        self.lock.release()
        return url

    def dequeue(self):
        while True:
            url = self.pop_queue()
            if not url:
                return None
            result = self.check(url, self.yourUrls)
            self.finalData.update(result)


    def start(self):
        self.event.onStart()
        print "BACKLINKCHECKER: Started checking links at {0}".format(datetime.now())
        threads = []
        for i in range(self.numberOfThreads):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        [t.join() for t in threads]
        self.event.onStop()
        print "BACKLINKCHECKER: Finished checking links at {0}".format(datetime.now())
        self.saveFile()


    def stop(self):
        self.abort = True
        print "BACKLINKCHECKER: Aborting..."

    def saveFile(self):
        try:
            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile.format(time.time())
            else:
                if not os.path.exists('./backlinkchecerresults'):
                    os.mkdir('./backlinkchecerresults')
                fileName = "./backlinkchecerresults/backlinkResult_{0}.csv".format(time.time())
            print "BACKLINKCHECKER: Writing results to file"
            with open(fileName,'a') as f:

                print >> f, 'Url,Your Link'
                for item in self.finalData:
                    print >> f, item
                    for v in self.finalData[item]:
                        print >>f, ",{0}".format(v)
            print "BACKLINKCHECKER: Successfully written to file {0}".format(os.path.abspath(fileName))

        except Exception, e:
            print "BACKLINKCHECKER: Error while saving to file {0}. Cause: {1}".format(os.path.abspath(fileName),e)


    def check(self, othersite, yoursites):
        if self.abort: return
        req = self.connectionManager.getSessionObject()
        #req = requests.Session()
        info = []
        try:
            print "BACKLINKCHECKER: Downloading page {0}".format(othersite)
            soup = BeautifulSoup(req.get(othersite).text)
            links = soup.findAll('a')
            links = [urljoin(othersite,link.get('href')) for link in links]

            for yoursite in yoursites:
                yoursiteRoot = urlparse.urlsplit(yoursite).netloc
                print urlparse.urlsplit(yoursite)
                for link in links:
                    if yoursite == link:
                        info.append(link)
                    elif len(yoursiteRoot) > 0 and yoursiteRoot in link:
                        info.append(link)
            print "BACKLINKCHECKER: {0} links found in site {1}".format(len(info),othersite)
        except Exception, e:
            print "BACKLINKCHECKER: There was an error while analyzing links in site: {0}. Reason {1}".format(othersite,e)
        return {othersite:info}
