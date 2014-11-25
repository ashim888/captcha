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
import requests

class ProxyChecker():
    status = {'alive':[],'dead':[]}
    hosts = []
    lock = threading.Lock()
    thread_count = 4

    abort = False

    def __init__(self,url, proxyFile, event, thread_count = 4, saveToFile = None):
        self.cm = ConnectionManager.ConnectionManager(proxyFile)
        self.url = url
        if thread_count > len(self.cm.proxies):
            thread_count = len(self.cm.proxies)
        self.thread_count = thread_count
        self.event = event
        self.saveToFile = saveToFile


    def pop_queue(self):
        proxy = None
        self.lock.acquire()
        if self.cm.proxies:
            proxy = self.cm.proxies.pop()

        self.lock.release()

        return proxy


    def dequeue(self):
        while True:

            temp = self.pop_queue()
            if not temp:
                return None

            proxy = ""
            if len(temp) == 4:
                proxy =  "http://" + temp[2] + ":" + temp[3] + "@" + temp[0] + ":" + temp[1]
            elif len(temp) == 2:
                proxy =  "http://" + temp[0] + ":" + temp[1]
            else:
                continue
            proxy = {'http':proxy}

            result = 'alive' if self.sendRequest(proxy) else 'dead'
            self.status[result].append(temp[0] + ':' + temp[1])

    def start(self):
        self.event.onStart()
        print "PROXYCHECKER: Started checking proxies at {0}".format(datetime.now())
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        [t.join() for t in threads]
        self.event.onStop()
        print "PROXYCHECKER: Finished checking proxies at {0}".format(datetime.now())
        print "PROXYCHECKER: Attempting to write the results to file"
        try:
            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile + '.alive'
            else:
                if not os.path.exists('./proxycheckerresults'):
                    os.mkdir('./proxycheckerresults')
                fileName = "./proxycheckerresults/proxychecker_alive{0}.txt".format(time.time())
            #print "PROXYCHECKER: Writing alive proxies to file: {0}".format(fileName)

            with open(fileName,"w") as f:
                for url in self.status['alive']:
                    print >> f, url
            print "SITECHECKER: Alive urls written to file: {0}".format(os.path.abspath(fileName))

            if self.saveToFile:
                fileName = self.saveToFile + '.dead'
            else:
                fileName = "./proxycheckerresults/proxychecer_dead{0}.txt".format(time.time())
            #print "SITECHECKER: Writing dead urls to file: {0}".format(fileName)
            with open(fileName,"w") as f:
                for url in self.status['dead']:
                    print >> f, url
            print "PROXYCHECKER: Dead urls written to file: {0}".format(os.path.abspath(fileName))
        except Exception, e:
            print "PROXYCHECKER: There was an error while saving the file. Details: {0}".format(e)
        self.status = None

    def stop(self):
        self.abort = True
        print "PROXYCHECKER: Aborting..."

    def sendRequest(self, proxy):
        if self.abort: return 0
        try:
            r = requests.Session()
            r.proxies = proxy
            r.timeout = 10
            r.get(self.url)
            print "PROXTCHECKER: {0}: OK".format(proxy['http'])
            return 1
        except:
            print "PROXYCHECKER: {0}: NOT OK".format(proxy['http'])
            return 0