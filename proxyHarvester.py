#-------------------------------------------------------------------------------
# Name:        proxyHarvester
# Purpose:
#
# Author:      Jangedoo
#
# Created:     19/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import threading
import ConnectionManager
import re
from datetime import datetime
import os
import time

class ProxyHarvester():
    proxies = []
    lock = threading.Lock()
    thread_count = 4
    urls = []

    abort = False

    def __init__(self, proxyFile, urlFile,event, thread_count = 4, saveToFile = None):
        self.cm = ConnectionManager.ConnectionManager(proxyFile)
        self._loadUrls(urlFile)
        self.thread_count = thread_count
        self.event = event
        self.saveToFile = saveToFile

    def _loadUrls(self, urlFile):
        with open(urlFile, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.urls.append(line)

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

            self.proxies += self.harvestProxy(url)

    def start(self):
        self.event.onStart()
        print "PROXYHARVESTER: Harvesing started at {0}".format(datetime.now())
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        [t.join() for t in threads]
        print "PROXYHARVESTER: Harvesting Complete at {0}".format(datetime.now())
        if not self.proxies:
            print "PROXYHARVESTER: No proxies harvested to save to the file"
        else:
            #save the proxies
            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile
            else:
                if not os.path.exists('./proxyharvesterresults'):
                    os.mkdir('./proxyharvesterresults')
                fileName ="./proxyharvesterresults/harvestedproxy{0}.txt".format(time.time())
            try:
                with open(fileName,"a") as f:
                    for proxy in self.proxies:
                        print>>f,proxy

                print "PROXYHARVESTER: Harvested proxies saved to {0}".format(os.path.abspath(fileName))
            except Exception, e:
                print "PROXYHARVESTER: Error while saving proxies to file {0}. Cause: {1}".format(os.path.abspath(fileName),e)
        self.event.onStop()

    def stop(self):
        self.abort = True

    def harvestProxy(self, url):
        if self.abort: return 0
        print "PROXYHARVESTER: Downloading page {0}".format(url)
        try:
            r = self.cm.getSessionObject()
            #r.timeout = 10
            resp = r.get(url)
            print "PROXYHARVESTER: Page from {0} downloaded".format(url)
            temp =re.findall(r'[0-9]+(?:\.[0-9]+){3}:\d{1,3}',resp.text)
            print "PROXYHARVESTER: {0} proxies harvested from {1}".format(len(temp),url)
            return temp
        except:
            print "PROXYHARVESTER: Error occured while downloadig page {0}".format(url)
