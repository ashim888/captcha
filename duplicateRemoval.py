#-------------------------------------------------------------------------------
# Name:        duplicateremoval
# Purpose:
#
# Author:      Jangedoo
#
# Created:     13/05/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import os

class DuplicateRemoval():
    urls = []
    def __init__(self, inputFile, outputFile=None):
        self.outputFile = outputFile
        with open(inputFile, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.urls.append(line)

    def removeDups(self):
        print "DUPLICATEREMOVER: Removing duplicates"
        return set(self.urls)

    def removeAndSave(self):
        fileName = ""
        if self.outputFile:
            fileName = outputFile
        else:
            if not os.path.exists('./dupremover'):
                os.mkdir('./dupremover')
            fileName = './dupremover/dupRemoved_{0}.txt'.format(time.time())

        print "DUPLICATEREMOVER: Saving to {0}".format(fileName)
        try:
            with open(fileName,'a') as f:
                for l in self.removeDups():
                    print >>f,l
            print "DUPLICATEREMOVER: Saved to {0}".format(os.path.abspath(fileName))
        except Exception, e:
            print "DUPLICATEREMOVER: Error while saving to file {0}".format(os.path.abs(fileName))

