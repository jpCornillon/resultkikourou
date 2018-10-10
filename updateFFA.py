#!/usr/bin/python3
# -*- coding: utf8
#
#####################################################
#
import os
import sys
import requests                                        # sudo dnf install python3-requests
from urllib.request import urlopen                     # sudo dnf install  python3-urllib
from bs4 import BeautifulSoup                          # sudo dnf install python3-beautifulsoup
import chardet                                         # detection encodage fichier (installé d'origine ???)
import sqlite3
#
#####################################################
# globales

####################### a modifier en fonction de son environement ####################
#FICDIR = '{}{}'.format(os.environ['HOME'], '/dropbox/kikourou/fichiers/source/')
REPWORK = '{}{}'.format(os.environ['HOME'], '/dropbox/kikourou_ori/fichiers/source/')
REPDEST = '{}{}'.format(os.environ['HOME'], '/dropbox/kikourou_ori/fichiers/csv/')
#######################################################################################
#

CSV = 'class;temps;nom;club;f1;cat\n'
BOLD = "\033[1m"
RESET = "\033[0;0m"
DB = sqlite3.connect('sql/baseFFA.db')
CURSOR = DB.cursor()


def majBase(url):
    # ligne ci-dessous péchées ici : https://stackoverflow.com/questions/4981977/how-to-handle-response-encoding-from-urllib-request-urlopen
    annee = '2018'
    courses = []
    req=urlopen(url)
    charset=req.info().get_content_charset()
    content=req.read().decode(charset)
    soup = BeautifulSoup(content, 'lxml')
    # table qui contient tous les lignes interessantes           
    table = soup.find('table', id='ctnResultats')
    for tr in table.findAll('tr'):
        td = [td for td in tr.findAll('td')]
        # Attention : certains résultats (icone Rés en jaune) ne sont pas intégres car ils n'ont pas 'lisResCom' mais 'listResInc' comme class
        if 'listResCom' in td[0].get('class', []):
            # recuperation du jour/mois 
            # bricolage pour les dates sous cette forme : 31-02/09
            if '-' in td[4].text and len(td[4].text) == 8:
                a_virer = td[4].text[3:]
                jj, mm = a_virer.split('/')[0][:2], a_virer.split('/')[1].replace('*', '')
            else:
                jj, mm = td[4].text.split('/')[0][:2], td[4].text.split('/')[1].replace('*', '')
            # recup du numero de course
            numero = td[8].a.get('href')[-6:]    
            # recup du departement, ville
            ville = td[10].text
            dept = td[14].text.replace('\xa0','xxx')
            titre = td[8].text
            # print('aa= {} mm={}, jj={}, dept={}, ville={}, numero= {}'.format(annee, mm, jj, dept, ville, numero))
            tup = (annee, mm, jj, dept, ville, numero, titre)
            courses.append(tup)
    return courses
    
def insertDB(d):
    try : 
        CURSOR.execute('''insert or replace into resultats (annee, mois, jour, departement, ville, numero, titre) 
            values(?, ?, ?, ?, ?, ?, ?)''', d)
        print('Ajouté dans la base : ', d)
        #DB.commit()
    except:
        print('Probleme pour : ', d)
    return

def nb_page(self):
    select = [ select for select in self.soup.findAll('select',{ "class" : "barSelect" }) ]
    try:
        options = select[0].findAll('option')
        nb = int(options[-1].get('value'))
    except:
        nb = 0
    return nb


def main():
    '''Le lien ci-dessous pointe sur la page des dernieres maj sur la base athlé FFA'''
    url = 'http://bases.athle.com/asp.net/accueil.aspx?frmbase=resultats'
    courses = majBase(url)
    for course in courses:
        insertDB(course)
    DB.commit()
    CURSOR.close()
    print('Nombre de courses trouvées :', len(courses))
    return 0

if __name__ == '__main__':
    main()
