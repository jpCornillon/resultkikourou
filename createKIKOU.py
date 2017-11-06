#!/usr/bin/python3
# -*- coding: utf8
#
import os
import sqlite3
import requests
from urllib.request import urlopen, ProxyHandler
from bs4 import BeautifulSoup
import re
from time import sleep

# fichier des regexp
from lib import ApplyRegex
from lib import rulesKikourou as kikourou
from lib import rulesBaseFFA  as FFA

#
#####################################################
# globales
# import pdb; pdb.set_trace()
FICDIR = '{}/dropbox/kikourou_ori/'.format(os.environ['HOME'])
BOLD = "\033[1m"
RESET = "\033[0;0m"
#
#####################################################

def lec_html():
    '''lecture/extraction des liens de la page résultat de chez kikourou'''
    # A VOIR POUR EVITER LES PROBLEMES D ENCODAGE
    #req=urlopen(self.url.format(page))
    #charset=req.info().get_content_charset()
    #content=req.read().decode(charset)

    URL = FICDIR+'/fichiers/source/kikourou_files/resultats.htm'
    html = open(URL, 'rb')
    soup = BeautifulSoup(html, 'lxml')
    return [ s.get('href') for s in soup.select("body td > a") if 'calendrier' in s.get('href') ]

def lec_specCourse(course):
    ''' recup infos chez kikourou'''
    url = 'http://www.kikourou.net{}#ongletinfo'.format(course)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', { 'class' : 'contenu-texte'})
    lieuCourse = div.find('a').text
    datas = [ data.previous_sibling for data in div.findAll('br') if '\n' not in data]
    print(datas)
    dateCourse = trtDate(datas[1])
    depCourse = trtDepartement(datas[2].lstrip())
    kmCourse = datas[3]
    return dateCourse + '{};{}'.format( lieuCourse, depCourse )

def trtDate(dat):
    datas = dat.split()
    jj = datas[1]
    mois = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre' ]
    dicMois = dict(zip(mois,[i for i in range(1, 13)] ))
    mm = dicMois[datas[2].replace('û','u').replace('ê', 'e').replace('é', 'e')]
    aa = datas[3]
    return '{};{};{};'.format(aa, mm, jj)

def trtDepartement(dpt):
    (r';(V[1-5])(-H);',  r';\1M;', True)
    dept=re.sub(r'\(([0-9][0-9]).*$', r'\1', dpt, flags=re.IGNORECASE)
    return dept


def sup_accent(ligne):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'] }
        for (char, accented_chars) in accents.items():
            for accented_char in accented_chars:
                ligne = ligne.replace(accented_char, char)
        return ligne


def main():
    f = ApplyRegex(FFA.patterns)
    #tous les liens qui pointent vers un fichier KiKourou
    #links = list(set(lec_html()))
    links = lec_html()
    import pdb; pdb.set_trace()
    # links.sort()
    #links = list(set(links))
    with open('allcourseskikou.csv', 'w') as f:
        for l in links:
            '''link_courses_kikou : liste des courses chez kikourou'''
            fic, ext = os.path.splitext(l)
            fic = fic.split('/')[-1]
            datas = lec_specCourse(l)
            f.write('{}\n'.format(datas))
#
#####################################################
#
if __name__ == '__main__':
    main()
#
#####################################################
