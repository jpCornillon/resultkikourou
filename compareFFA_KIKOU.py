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
DB = sqlite3.connect('sql/baseFFA.db')
CURSOR = DB.cursor()
#
#####################################################

def lec_html():
    '''lecture/extraction des liens de la page résultat de chez kikourou'''
    URL = FICDIR+'/fichiers/source/kikourou_files/resultats.htm'
    html = open(URL, 'r')
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

def searchFFA(d):   
    annee, mois, jour, departement = d
    sqlbase = 'select annee, mois, jour, ville, titre, numero, departement from resultats where '
    where = ' annee={} and mois={} and jour={} and departement={}'.format(annee, mois, jour, "'{0:03d}'".format(int(departement)))
    sql = sqlbase + where
    CURSOR.execute(sql)
    return CURSOR
    #  for row  in CURSOR:
        #  print('\t - {:04}-{:02}-{:02}  {:25}: {} N°{:6} ({:3})'.format(*row))


def main():
    f = ApplyRegex(FFA.patterns)
    # tous les liens qui pointent vers un fichier KiKourou
    kikous = open('allcourseskikou.csv').readlines()
    kikous.sort()
    #kikous = [ k.strip() for k in set(kikous) ]
    for k in kikous:
        i = 0
        l3 = ''
        annee, mois, jour, ville, departement, nom_kikou = k.split(';')
        # l1 = '\n' + '*'*(42 + len(ville) + len(mois) + len(jour))
        nom_kikou = nom_kikou.replace('/calendrier/', '')[:-6].strip()
        l2 = '\nRecherche pour {} ({}) à la date du {}-{}-{} ({}):'.format(ville, departement.strip(), annee, mois, jour, nom_kikou)
        d = (annee, mois, jour, departement)
        cursor = searchFFA(d)
        for row  in cursor:
            i += 1
            l3 += '\n\t - {:04}-{:02}-{:02}  {:25}: {} N°{:6} ({:3})'.format(*row)
        if i > 0 : print(l2 + l3 )
#
#####################################################
#
if __name__ == '__main__':
    main()
#
#####################################################
