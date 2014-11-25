from bs4 import BeautifulSoup
from operator import itemgetter
import re
def analyzePlatform(html):
    s = BeautifulSoup(html)
    scores = {'bellabook':0,'akobook':0,'easyphp':0,'ricar':0,'phpbook':0 ,}

    #Bellabook footprints
    if s.find('a',{'href':'http://www.jemjabella.co.uk/scripts'}):
        scores['bellabook'] += 1
    if s.find('form',{'action':'sign.php'}):
        scores['bellabook'] += 1
    if s.find('label', {'for':'human'}):
        scores['bellabook'] += 1

    #Akobook footprints


    #phpBOOK footprints
    if s.find('form',{'action':re.compile('guestbook.php')}):
        scores['phpbook'] += 1
    if s.find('input',{'name':'in[name]'}):
        scores['phpbook'] +=1

    #Ricar footprints
    if s.find('form',{'name':'signform','action':'save_comment.php'}):
        scores['ricar'] += 1
    if s.find('input',{'name':'ip_guest'}):
        scores['ricar'] += 1
    if s.find('a',{'href':'http://ricargbook.adrielmedia.com'}):
        scores['ricar'] += 1

    val = sorted(scores.items(), key=itemgetter(1), reverse=True)[:1][0]
    if val[1] == 0:
        return 'unknown'
    else:
        return val[0]

