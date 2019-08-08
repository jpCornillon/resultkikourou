#!/usr/bin/python3
# -*- coding: utf8
#
'''TODO :
- traiter les adresses de la forme : http://templiers.livetrail.net/
- possibilité de traiter une seule epreuve de la course (ex : uniquement le 72 des Templiers
''' 

'''Sur le site de livetrail :
- selectionner le classement de la course recherchée
- une fois que les coureurs sont affichés, 'ctrl + maj +i' (inspecter le code)
- onglet source, sur la page recherchée (classement.php), il faut 
récuperer les donnees 'Form Data' puis les passer a curl (wget) pour 
charger le contenu
curl --data 'course=chro57&cat=scratch&pays=all'  http://www.livetrail.net/histo/ardechois2016/classement.php
<ou>
wget --no-proxy   --post-data 'course=ultra&cat=scratch&pays=all' http://www.livetrail.net/histo/thp2016/classement.php
1 - wget du fichier generale, exemple pour InterlacTrail :  http://www.livetrail.net/histo/interlac_2016/classement.php
 a linterieur du fichier (index.html) on trouve les differentes epreuves (balise <e><id>
2 c'est cet id qu'il faut passer au futur wget --data 'course=ID&&cat....' 
'''
#
import os
import sys
import re
import requests
import subprocess
import urllib.parse
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from lib import Tools
#
# globales
####################### a modifier en fonction de son environement ####################
REPWORK = '{}{}'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/source/')
REPDEST = '{}{}'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/csv/')
BOLD = "\033[1m"
RESET = "\033[0;0m"
# import pdb; pdb.set_trace()
#######################################################################################
#
class Epreuve(object):
    "Epreuve est composée de x courses"""
    lienCourse = 'http://www.livetrail.net/histo/{lut2016}/classement.php'

    def __init__(self, lien):
        # suppression de dernier / de l'url
        if lien[-1] == '/': lien = lien[:-1]
        self.lien = lien
        if lien.startswith('http://livetrail.net/histo'):
            self.nomEpreuve = lien.replace('http://livetrail.net/histo/','')
            self.type_lien=1
        elif lien.startswith('https://livetrail.net/histo'):
            self.nomEpreuve = lien.replace('https://livetrail.net/histo/','')
            self.type_lien=1
        elif lien.endswith('livetrail.net'):   
            # utilisation pour suppression "httpd://" ou "https://"
            self.nomEpreuve = re.sub(r'^.*://', '', lien).replace('.livetrail.net', '')
            # self.nomEpreuve = lien.replace('http://','').replace('.livetrail.net', '')
            self.type_lien=2
        elif lien.endswith('livetrail.run'):   
            self.nomEpreuve = re.sub(r'^.*://', '', lien).replace('.livetrail.run', '')
            # self.nomEpreuve = lien.replace('http://','').replace('.livetrail.run', '')
            self.type_lien=2
        elif lien.startswith('https://livetrail.net/live/'):   
            self.nomEpreuve = lien.replace('https://livetrail.net/live/','')
            self.type_lien=3
        else:
            print('Lien pourri !!!!')
            exit(1)
        self.courses = self.find_course()

    def find_course(self):
        '''recuperation des differentes course pour cette epreuve'''
        epreuves = []
        html = urlopen(self.lien)
        # urllib.request.Request(url, datas = datas)
        soup = BeautifulSoup(html, 'lxml')
        for courses in soup.findAll('e'):
            if courses.get('id'):
                epreuves.append(Course((self.nomEpreuve, courses.get('id'), courses.get('titre'), courses.get('sstitre'), self.type_lien)))
            #import pdb; pdb.set_trace()
        return epreuves


class Course(object):
    """docstring for Course"""

    def __init__(self, arg):
        self.nomCourse = arg[0]
        self.course = arg[1]
        self.lib = arg[2]
        self.km_deniv = arg[3]
        self.type_lien = arg[4]
        self.data = self.make_data()
        if self.type_lien == 1:
            self.lienCourse = 'https://livetrail.net/histo/{}/classement.php'.format(self.nomCourse)
            #self.lienCourse = 'http://livetrail.net/histo/{}/classement.php'.format(self.nomCourse)
        elif self.type_lien == 2:
            #self.lienCourse = 'http://{}.livetrail.net/classement.php'.format(self.nomCourse)
            self.lienCourse = 'http://{}.livetrail.run/classement.php'.format(self.nomCourse)
        elif self.type_lien == 3:
            self.lienCourse = 'https://livetrail.net/live/{}/classement.php'.format(self.nomCourse)
        else:
            print('Mauvais type de lien !!!!')
            exit(1)

    def make_data(self):
        datas = dict(zip(['course', 'cat', 'pays'], [self.course, 'scratch', 'all']))
        data = urllib.parse.urlencode(datas)
        data = data.encode('utf-8')
        return data

    def __str__(self):
        return '{} - {} - {} - {} - {}'.format(self.nomCourse, self.course, self.lib, self.km_deniv, self.lienCourse)


def make_dic_fic(fic):
    dFic = {}
    dFic['ficcsv'] = '{}{}.csv'.format(REPWORK, fic)
    dFic['fickikou'] = '{}{}.csv'.format(REPDEST, fic)
    return dFic

def main(argv):
    if 'auto' in argv:
        auto = True
    else:
        auto = False
    #chargement des outils
    tools = Tools(auto)
    
    lnk = input('Lien : ')
    epreuve = Epreuve(lnk)
    for e in epreuve.courses:
        if e.course.lower() not in ['relais']:
            print(BOLD + '{} --> {} '.format(e.nomCourse, e.course) + RESET) 
            tools.fichiers = make_dic_fic('{}_{}'.format(e.nomCourse, e.course))
            tools.coureurs = tools.htmtoliste(e.lienCourse, e.data)
        
            if tools.checkCoureurs(tools.coureurs):
                tools.writeCsv(tools.coureurs, tools.fickikou)
                print(BOLD, "{} --> course {} traitée".format(e.nomCourse, e.course), RESET)
                print(BOLD, "Fichier {} pret à tranférer sur KiKourou".format(tools.fickikou), RESET)
                # sauvegarde du htm
                fic = 'mv {} {}/sv_fic_source'
                #sv =  os.system(fic.format(tools.fichtm, REPWORK))
            else:
                tools.writeCsv(tools.coureurs, tools.ficcsv)
                print(BOLD, "Fichier {} pourri".format(tools.ficcsv), RESET)
                for cle, valeur in tools.anos.items():
                    print(BOLD, "\nAnomalie de type : ", cle, RESET)
                    for ano in valeur:
                        print('\t{}'.format(ano))                
        else:
            '''on vire les 'relais' '''
            print(BOLD + '\n{} --> {} non traité !!!'.format(e.nomCourse, e.course) + RESET) 

#
#####################################################
#
if __name__ == '__main__':
    main(sys.argv[1:])
#
#####################################################

'''
HowTo : recuperer les coureurs en postant 3 arguments :

<python3>
datas = {'course': '19km', 'cat': 'scratch', 'pays': 'all'}
data = urllib.parse.urlencode(datas)
data = data.encode('utf-8')
req = urllib.request.Request('http://www.livetrail.net/histo/traildesforts_2016/classement.php', data)
response = urllib.request.urlopen(req)
html = response.read()
soup = BeautifulSoup(html, 'lxml')

<bash>
wget --post-data 'cat=scratch&pays=all&course=17km' http://www.livetrail.net/histo/interlac_2016/classement.php
'''
