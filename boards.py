import urllib2
from lxml import html
import re
import csv
import unicodecsv
from cStringIO import StringIO

titleKeywords = ['director','officer','ceo','president','secretary','chairman','board','chief']

class secParser():
    def __init__(self,pageURL):
        self.pageURL = pageURL
        page = urllib2.urlopen(pageURL, timeout = 10000)
        print "[INFO] page opened"
        self.pageContent = page.read()
        print "[INFO] html loaded"
        self.boards = []

        
    def htmlParser(self):
        pageTree = html.fromstring(self.pageContent)
        print "page parsed!"
        tdTexts =  pageTree.xpath("//td/descendant::*/text()")
        cleanTexts = [eachText.strip() for eachText in tdTexts if eachText.strip()]
        for i in range(1,len(cleanTexts)):
            if ('/s/' in cleanTexts[i] and (i+1) < len(cleanTexts)):
                title = []
                title = [cleanTexts [i+1] for eachKeyword in titleKeywords if eachKeyword in cleanTexts [i+1].lower()]
                if (title):
                    self.boards.append([self.pageURL,cleanTexts[i].replace('/s/',''),cleanTexts [i+1]])
                elif (i+2) < len(cleanTexts):
                    title = [cleanTexts [i+2] for eachKeyword in titleKeywords if eachKeyword in cleanTexts [i+2].lower()]
                    if (title):
                        self.boards.append([self.pageURL,cleanTexts[i].replace('/s/',''),cleanTexts [i+2]])
                        
                    
                
    def textParser(self):
        signatures1 = re.findall("/s/.*",self.pageContent)
        cleanTexts1 = [s.strip() for sign in signatures1 for s in sign.split("  ") if s.strip()]
        signatures2 = re.findall("/s/.*\n.*-+\n.*\n.*",self.pageContent)
        cleanSignatures2 = [re.sub('-+','',eachSign) for eachSign in signatures2]
        cleanTexts2 = [s.strip() for sign in cleanSignatures2 for s in sign.split("\n") if s.strip()]
        cleanTexts = cleanTexts1 + cleanTexts2
        for i in range(1,len(cleanTexts)):
            if ('/s/' in cleanTexts[i] and (i+1) < len(cleanTexts)):
                title = []
                title = [cleanTexts [i+1] for eachKeyword in titleKeywords if eachKeyword in cleanTexts [i+1].lower()]
                if (title):
                    self.boards.append([self.pageURL,cleanTexts[i].replace('/s/',''),cleanTexts [i+1]])
                elif (i+2) < len(cleanTexts):
                    title = [cleanTexts [i+2] for eachKeyword in titleKeywords if eachKeyword in cleanTexts [i+2].lower()]
                    if (title):
                        self.boards.append([self.pageURL,cleanTexts[i].replace('/s/',''),cleanTexts [i+2]])
                            
    def extractBoard(self):
        self.htmlParser()
        if not(self.boards):
            self.textParser()
        print self.boards


def storeToCsv(array_to_be_saved,filename_including_path):
    f = StringIO()
    w = unicodecsv.writer(f, encoding='utf-8',delimiter=';',quotechar='"')
    for each_row in array_to_be_saved:
        w.writerow(each_row)
    with open(filename_including_path, 'a') as csvfile:
        csvfile.write(f.getvalue())
    f.close()
    return 0        
        
def runClass():
    #csvInputPath = raw_input('Enter the path to the input csv file e.g. C:\csv files\10KLinks.csv')
    csvInputPath = "C:\\Users\\mhaghbaali1\\Desktop\\2005_input.csv"
    #csvOutputPath = raw_input('Enter the path to the output csv file e.g. C:\csv files\boardMembersSEC.csv')
    csvOutputPath = "C:\\Users\\mhaghbaali1\\Desktop\\2005_output.csv"
    inputFile = open(csvInputPath,'rb')
    paths = csv.reader(inputFile)
    for path in paths:
        secPage = secParser(path[0])
        secPage.extractBoard()
        if (secPage.boards):
            storeToCsv(secPage.boards,csvOutputPath)
    
if __name__ == "__main__":
    runClass()