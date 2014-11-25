import spinner
import random
import os
class DataManager:
    def __init__(self, nameFile, emailFile, websiteFile, commentFile):
        self.nameFile = nameFile
        self.emailFile = emailFile
        self.websiteFile = websiteFile
        self.commentFile = commentFile
        self._loadFiles()

        self.currentWebsiteIndex = 0

    def _loadFiles(self):
        try:
            with open(os.path.join(self.nameFile)) as f:
                self.names = f.read()
            with open(self.emailFile,"r") as f:
                self.emails = f.read()
            with open(self.websiteFile) as f:
                self.websites = [l for l in (line.strip() for line in f) if l]
            with open(self.commentFile) as f:
                self.comments = f.read()
        except Exception as e:
            print e


    def getValue(self, variable):
        if variable == 'name':
            return spinner.spin(self.names)
        elif variable == 'email':
            return spinner.spin(self.emails)
        elif variable == 'comment':
            return spinner.spin(self.comments)
        elif variable == 'website':
            return random.choice(self.websites)
