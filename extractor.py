#-------------------------------------------------------------------------------
# Name:        extractor
# Purpose:      for extracting urls and emails from file or websites
#
# Author:      Jangedoo
#
# Created:     24/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from datetime import datetime
import time
import os
import re
import ConnectionManager
import threading

#Thread adjustment is done on start function

class Extractor:
    urlFinder = re.compile(r'(https*://.+?)["|\s]',re.DOTALL|re.MULTILINE)

    email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')

    finalEmails = []
    finalUrls = []

    def __init__(self, inputFile, connectionManager,
                 event, numberOfThreads = 3,
                 isLocal = False, extractEmail = False,
                 extractUrl = True, saveToFile = None):

        print "Uncomment self.event stuffs and remove this after everything is complete"
        self.connectionManager = connectionManager
        self.event = event
        self.isLocal = isLocal
        self.extractEmail = extractEmail
        self.extractUrl = extractUrl
        self.saveToFile = saveToFile
        self.inputFile = inputFile
        self.numberOfThreads = numberOfThreads
        self.abort = False
        self.lock = threading.Lock()

        if not os.path.exists('./extractorresults'):
                    os.mkdir('./extractorresults')


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
            result = self.extract(url)
            print result
            if result and result[1]:
                self.finalEmails += result[1]
            if result and result[0]:
                self.finalUrls += result[0]

    def start(self):
        #self.event.onStart()
        print "EXTRACTOR: Started extracting... {0}".format(datetime.now())
        if self.isLocal:
            result =self.extractLocal(self.inputFile)
            self.finalEmails = result[1]
            self.finalUrls = result[0]
        else:
            self.urls = self._loadData(self.inputFile)
            if self.numberOfThreads > len(self.urls):
                self.numberOfThreads = len(self.urls)
            threads = []
            for i in range(self.numberOfThreads):
                t = threading.Thread(target=self.dequeue)
                t.start()
                threads.append(t)

            [t.join() for t in threads]
        #self.event.onStop()
        print "EXTRACTOR: Finished extracting emails/urls at {0}".format(datetime.now())
        self.saveFile()



    def stop(self):
        self.abort = True

    def saveFile(self):
        try:
            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile.format(time.time())
            else:
                fileName = "./extractorresults/extract_{0}_{1}.txt"
            print "EXTRACTOR: Writing urls to file"
            if self.extractUrl:
                f =fileName.format('urls',time.time())
                with open(f,'a') as writer:
                    for item in self.finalUrls:
                        print >> writer, item
                print "EXTRACTOR: Urls successfully written to file {0}".format(os.path.abspath(f))
            if self.extractEmail:
                f = fileName.format('emails',time.time())
                with open(f,'a') as writer:
                    for item in self.finalEmails:
                        print >> writer, item
                print "EXTRACTOR: Emails successfully written to file {0}".format(os.path.abspath(f))

        except Exception, e:
            print "EXTRACTOR: Error while saving to file {0}. Cause: {1}".format(os.path.abspath(fileName),e)

    def extract(self, data):
        if self.isLocal:
            return self.extractLocal(data)
        else:
            return self.extractRemote(data)

    def extractLocal(self, inputFile):
        try:
            text = None
            with open(inputFile, 'r') as f:
                text = f.read()
        except:
            print "EXTRACTOR: Error while opening file {0}".format(inputFile)

        if text: return self._extract(text)



    def extractRemote(self, url):
        if self.abort: return
        html = None
        try:
            html = self.connectionManager.getSessionObject().get(url).text
        except:
            print "EXTRACTOR: Error while downloading page {0}".format(url)
        if html: return self._extract(html)

    def _extract(self, content):
        email_matches = []
        url_matches = []

        if self.extractUrl:
            print "EXTRACTOR: Parsing urls"
            url_matches += self.urlFinder.findall(content)

        if self.extractEmail:
            email_matches=self.email_pattern.findall(content)

        print "EXTRACTOR: Total urls = {0} and total emails = {1}".format(len(url_matches), len(email_matches))
        return (url_matches, email_matches)


#test = Extractor(r'C:\Users\Jangedoo\Desktop\url.txt',ConnectionManager.ConnectionManager(None),None,1)
#test.start()