#-------------------------------------------------------------------------------
# Name:        statuschecker
# Purpose:
#
# Author:      Jangedoo
#
# Created:     19/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import subprocess
import threading
import ConnectionManager
import time
import os
from datetime import datetime

class SiteStatusChecker():
    status = {'alive':[],'dead':[]}
    hosts = []
    lock = threading.Lock()
    thread_count = 4
    urls = []

    abort = False

    def __init__(self,urlFile, proxyFile, event, thread_count = 4, saveToFile = None):
        self.cm = ConnectionManager.ConnectionManager(proxyFile)
        self._loadUrls(urlFile)
        if thread_count > len(self.urls):
            thread_count = len(self.urls)
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
            result = 'alive' if self.sendRequest(url) else 'dead'
            self.status[result].append(url)

    def start(self):
        self.event.onStart()
        print "SITECHECKER: Started checking sites at {0}".format(datetime.now())
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        [t.join() for t in threads]
        self.event.onStop()
        print "SITECHECKER: Finished checking sites at {0}".format(datetime.now())
        print "SITECHECKER: Attempting to write the results to file"
        try:
            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile + '.alive'
            else:
                if not os.path.exists('./statuscheckerresults'):
                    os.mkdir('./statuscheckerresults')
                fileName = "./statuscheckerresults/sitechecker_alive{0}.txt".format(time.time())
            print "SITECHECKER: Writing alive urls to file: {0}".format(fileName)

            with open(fileName,"w") as f:
                for url in self.status['alive']:
                    print >> f, url
            #print "SITECHECKER: Alive urls written to file: {0}".format(os.path.abspath(fileName))

            if self.saveToFile:
                fileName = self.saveToFile + '.dead'
            else:
                fileName = "./statuscheckerresults/sitechecker_dead{0}.txt".format(time.time())
            #print "SITECHECKER: Writing dead urls to file: {0}".format(fileName)
            with open(fileName,"w") as f:
                for url in self.status['dead']:
                    print >> f, url
            print "SITECHECKER: Dead urls written to file: {0}".format(os.path.abspath(fileName))
        except Exception, e:
            print "SITECHECKER: There was an error while saving the file. Details: {0}".format(e)
        self.status = None

    def stop(self):
        self.abort = True
        print "SITECHECKER: Aborting..."

    def sendRequest(self, url):
        if self.abort: return 0
        try:
            r = self.cm.getSessionObject()
            r.get(url)
            print "SITECHECKER: {0}: OK".format(url)
            return 1
        except:
            print "SITECHECKER: {0}: NOT OK".format(url)
            return 0
