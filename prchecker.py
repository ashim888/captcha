import ConnectionManager
import csv
import re
import os
import thread
import time
class PrChecker:
    def __init__(self, cm, event, checkPr=True, checkAlexa=True, saveToFile = None):
        self.cm = cm
        self.event = event
        self.abort = False
        self.saveToFile = saveToFile
        self.checkPr = checkPr
        self.checkAlexa = checkAlexa

    def _HashURL (self,url):
        SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE."
        Result = 0x01020345
        for i in range(len(url)) :
            Result ^= ord(SEED[i%len(SEED)]) ^ ord(url[i])
            Result = Result >> 23 | Result << 9
            Result &= 0xffffffff
        return '8%x' % Result

    def getpr(self,url):
        url = url.strip("\a\b\f\n\r\t\v")
        googleurl = 'http://toolbarqueries.google.com/tbr?client=navclient-auto&features=Rank&ch='+self._HashURL(url)+'&features=Rank&q=info:'+url
        req = self.cm.getSessionObject()
        response = req.get(googleurl)
        data = response.text
        status = response.status_code
        pr = data.split(":")[-1].strip('\n')
        if len(pr) == 0 or status != 200:
            pr = '-1'
        return pr

    def get_alexa_rank(self, url):
        try:

            data = self.cm.getSessionObject().get('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)).text
            reach_rank = re.findall("REACH[^\d]*(\d+)", data)
            if reach_rank: reach_rank = reach_rank[0]
            else: reach_rank = -1

            popularity_rank = re.findall("POPULARITY[^\d]*(\d+)", data)
            if popularity_rank: popularity_rank = popularity_rank[0]
            else: popularity_rank = -1

            return int(popularity_rank), int(reach_rank)

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception, e:
            print e
            return -1, -1

    def getstatsFile(self, urlFile):
        self.event.onStart()
        try:
            if not urlFile:
                raise IOError('File not supplied')
            prInfo = {}
            self.abort = False
            with open(urlFile,"r") as f:
                for url in (line.strip() for line in f):
                    if self.abort: break
                    if not url: continue
                    try:
                        pr = -1
                        alexa_popularity_rank = -1
                        alexa_reach_rank = -1
                        if self.checkPr:
                            pr = self.getpr(url)
                            print "GOOGLE: Url:{0}, PR:{1}".format(url, pr)
                        if self.checkAlexa:
                            alexa_popularity_rank, alexa_reach_rank = self.get_alexa_rank(url)
                            print "ALEXA: Url:{0}, Popularity Rank:{1}, Reach Rank: {2}".format(url, alexa_popularity_rank, alexa_reach_rank)

                        prInfo[url] = (pr,alexa_popularity_rank, alexa_reach_rank)
                    except Exception, e:
                        print "Error while cheking stats of url {0}. Cause: {1}".format(url, e)

            print "Check Complete"

            fileName = ""
            if self.saveToFile:
                fileName = self.saveToFile
            else:
                if not os.path.exists('./prchecherresults'):
                    os.mkdir('./prchecherresults')
                fileName = "./prchecherresults/prcheckerresult_{0}.csv".format(time.time())

            with open(fileName, "a") as f:
                writer = csv.writer(f)
                writer.writerow(('Url','PageRank','Alexa Popularity Rank','Alexa Reach Rank'))
                csv.writer(f).writerows((k,) + v for k, v in prInfo.iteritems())

            print "File saved to {0}".format(os.path.abspath(fileName))
        except IOError, e:
            print "Error while dealing with file. If check is already complete then the error occured while saving the results to the CSV file. Reason {0}".format(e)

        except Exception, e:
            print "Error while checking PR. Reason: {0}. Aborting...".format(e)

        self.event.onStop()

'''
cm = ConnectionManager.ConnectionManager(None)
checker = PrChecker(cm)
checker.getstatsFile(r'C:\Users\Jangedoo\Desktop\url.txt', checkPr=True)
'''