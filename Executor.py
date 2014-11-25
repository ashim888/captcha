#-------------------------------------------------------------------------------
# Name:        Executor
# Purpose:
#
# Author:      Jangedoo
#
# Created:     09/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Queue
import bellabook
import phpbook
import ricar
import requests
import platformanalyzer
import threading
from datetime import datetime
class Executor:
    def __init__(self, urlsFile, connectionManager, dataManager, event, thread_count = 4):
        self.urlsFile = urlsFile
        self.connectionManager = connectionManager
        self.dataManager = dataManager
        self.event = event
        self.urls= []
        self.thread_count = thread_count
        self.lock = threading.Lock()
        self.shouldAbort = False
        self._loadUrls()
        if len(self.urls) < self.thread_count:
            self.thread_count = len(self.urls)

        self.totalUrls = len(self.urls)
        self.currentProgress = 0

    def _loadUrls(self):
        with open(self.urlsFile, "r") as f:
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
            self.execute(url)

    def start(self):
        self.totalUrls = len(self.urls)
        self.currentProgress = 0
        self.event.onStart()
        print "COMMENTPOSTER: Started commenting at {0}".format(datetime.now())
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.start()
            threads.append(t)

        [t.join() for t in threads]
        self.event.onStop()
        print "COMMENTPOSTER: Finished commenting at {0}".format(datetime.now())


    def execute(self, url):
        ev = self.event
        conn = self.connectionManager.getSessionObject()
        try:
            resp = conn.get(url)
            platform = platformanalyzer.analyzePlatform(resp.text)
            ev.onLogMessage(('COMMENTPOSTER: ' + url + " identified as " + platform))
            if platform == 'bellabook':
                ev.onLogMessage(('COMMENTPOSTER' + bellabook.bellabook(conn, resp, self.dataManager)))
            elif platform == 'phpbook':
                ev.onLogMessage(('COMMENTPOSTER' + phpbook.phpbook(conn, resp, self.dataManager)))
            elif platform == 'ricar':
                ev.onLogMessage(('COMMENTPOSTER' + ricar.ricar(conn, resp, self.dataManager)))
            elif platform == 'unknown':
                ev.onLogMessage("COMMENTPOSTER: Unknown platform")
        except:
            ev.onLogMessage(("COMMENTPOSTER: Error downloading the page " + url))

        self.currentProgress += 1
        ev.onProgressChange((self.currentProgress*100)/self.totalUrls)


    def stop(self):
        self.shouldAbort = True