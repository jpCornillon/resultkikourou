#!/usr/bin/python3
# -*- coding: utf8
#
#####################################################
#
import os
import sys
from time import sleep
import requests                                        # sudo dnf install python3-requests
from urllib.request import urlopen                     # sudo dnf install  python3-urllib
from bs4 import BeautifulSoup                          # sudo dnf install python3-beautifulsoup
import chardet                                         # detection encodage fichier (installé d'origine ???)
import sqlite3
# classes locales
from lib import Tools
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

class BaseFFA(object):
    def __init__(self, url):
        super(BaseFFA, self).__init__()
        self.db = self.createDB()
        self.annee = url[-4:]
        self.url = url
        self.nomFic = 'a_virer.csv'
        html = urlopen(self.url)
        self.soup = BeautifulSoup(html, 'lxml')
        self.nb_pages = self.nb_page()
        # url = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison={}frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement=&frmeprrch=&frmclub=&frmdate_j1=1&frmdate_m1=1&frmdate_a1={}&frmdate_j2=30&frmdate_m2=12&frmdate_a2={}&frmposition=0'
        # html = urlopen(url.format(annee, annee, annee, 0))
        # url = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison=2017&frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement=&frmeprrch=&frmclub=&frmdate_j1=1&frmdate_m1=9&frmdate_a1=2017&frmdate_j2=30&frmdate_m2=12&frmdate_a2=2017'

    def createDB(self):
        db = sqlite3.connect('sql/baseFFA.db')
        try:
            cursor = db.cursor()
            # creation de la table resultats
            cursor.execute('''create table if not exists resultats (
                annee integer,
                mois integer,
                jour integer,
                departement text,
                ville text,
                numero integer,
                titre text),
                primary key ('annee', 'mois', 'jour', 'departement', 'ville', 'numero')''')
            db.commit()
            cursor.close()
            db.close()
        except:
            print('Base/Table déja créees !!!!')
        return db

    def createCSV(self):
        with open(self.nomFic, 'w') as fic:
            self.url = self.url + '&frmposition={}'
            for page in range(self.nb_pages + 1):
                sleep(1)
                print('----------------')
                print('Page {} sur {}'.format(page, self.nb_pages))
                print('----------------')
                #url = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison={}&frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement=&frmeprrch=&frmclub=&frmdate_j1=1&frmdate_m1=1&frmdate_a1={}&frmdate_j2=30&frmdate_m2=12&frmdate_a2={}&frmposition={}'
                # url = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison={}&frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement=&frmeprrch=&frmclub=&frmdate_j1=1&frmdate_m1=9&frmdate_a1={}&frmdate_j2=30&frmdate_m2=12&frmdate_a2={}&frmposition={}'
                # html = urlopen(url.format(self.annee, self.annee, self.annee, page)).decode('utf-8')
                # ligne ci-dessous péchées ici : https://stackoverflow.com/questions/4981977/how-to-handle-response-encoding-from-urllib-request-urlopen
                req=urlopen(self.url.format(page))
                charset=req.info().get_content_charset()
                content=req.read().decode(charset)
                soup = BeautifulSoup(content, 'lxml')
                #soup = BeautifulSoup(html, 'lxml')
                # table qui contient tous les lignes interessantes           
                table = soup.find('table', id='ctnResultats')
                # courses = {}
                for tr in table.findAll('tr'):
                    td = [td for td in tr.findAll('td')]
                    # Attention : certains résultats (icone Rés en jaune) ne sont pas intégres car ils n'ont pas 'lisResCom' mais 'listResInc' comme class
                    if 'listResCom' in td[0].get('class', []):
                        # recuperation du jour/mois 
                        jj, mm = td[4].text.split('/')[0][:2], td[4].text.split('/')[1].replace('*', '')
                        # recup du numero de course
                        numero = td[8].a.get('href')[-6:]    
                        # recup du departement, ville
                        ville = td[10].text
                        dept = td[14].text.replace('\xa0','xxx')
                        titre = td[8].text
                        print('aa= {} mm={}, jj={}, dept={}, ville={}, numero= {}'.format(self.annee, mm, jj, dept, ville, numero))
                        fic.write('{};{};{};{};{};{};{}\n'.format(self.annee, mm, jj, dept, ville, numero, titre))
        return True
    
    def insertDB(self):
        cursor = self.db
        problems = []
        with open(self.nomFic, 'r') as f:
            for line in f.readlines():
                try : #METTRE UN TRY ICI 
                    annee, mois, jour, departement, ville, numero, titre = line.strip().split(';')
                    d = (annee, mois, jour, departement, ville, numero, titre)  
                    cursor.execute('''insert or replace into resultats (annee, mois, jour, departement, ville, numero, titre) 
                        values(?, ?, ?, ?, ?, ?, ?)''', d)
                    #self.db.commit()
                except:
                    print('Probleme pour : ', line)
                    problems.append(line)
        self.db.commit()
        cursor.close()
        self.db.close()
        if len(problems) == 0:
            print('Pas de soucis !!!')
        else:
            for problem in problems: print(problem)
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
    # sur le site de la FFA : faire une recherche (Hors Stade) et copier l'adresse generée
    # ex : recherche 2017 - Hors stade - du 1/10/2017 au 30/12/2017
    # copier/coller l'@ du resultat au lancement de ce script
    # ATTENTION : pour le moment if faut que la rercherche retourne plus d'une page de resultat sinon la boucle se plante

    url = input('Lien : ')
    ffa = BaseFFA(url)
    # ffa.insertDB()
    # exit(1)
    if ffa.createCSV():
        # chargement de la base
        print('###### insertion dans la base #######')
        ffa.insertDB()
        #ffa.ficCSV()
    return 0

if __name__ == '__main__':
    main()
