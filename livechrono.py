#!/usr/bin/python3
# -*- coding: utf8
#
'''Sur le site de l-chrono :
- selectionner le classement de la course recherchée
- une fois que les coureurs sont affichés, 'ctrl + maj +i' (inspecter le code)
- onglet source, sur la page recherchée (classement.php), il faut 
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
REPWORK = '{}{}'.format(os.environ['HOME'], '/dropbox/kikourou_ori/fichiers/source/')
REPDEST = '{}{}'.format(os.environ['HOME'], '/dropbox/kikourou_ori/fichiers/csv/')
BOLD = "\033[1m"
RESET = "\033[0;0m"
# import pdb; pdb.set_trace()
#######################################################################################
#
class Epreuve(object):
    "Epreuve est composée de x courses"""
    lienCourse = 'http://www.livetrail.net/histo/{lut2016}/classement.php'

    def __init__(self, lien):
        self.lien = lien
        if 'http://www.livetrail' in lien:
            self.nomEpreuve = lien[:-1].replace('http://www.livetrail.net/histo/','')
        elif 'http://livetrail'  in lien:   
            self.nomEpreuve = lien[:-1].replace('http://livetrail.net/histo/','')
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
                epreuves.append(Course((self.nomEpreuve, courses.get('id'), courses.get('titre'), courses.get('sstitre'))))
        return epreuves


class Course(object):
    """docstring for Course"""

    def __init__(self, arg):
        self.nomCourse = arg[0]
        self.course = arg[1]
        self.lib = arg[2]
        self.km_deniv = arg[3]
        self.data = self.make_data()
        self.lienCourse = 'http://www.livetrail.net/histo/{}/classement.php'.format(self.nomCourse)

    def make_data(self):
        datas = dict(zip(['course', 'cat', 'pays'], [self.course, 'scratch', 'all']))
        data = urllib.parse.urlencode(datas)
        data = data.encode('utf-8')
        return data


def make_dic_fic(fic):
    dFic = {}
    dFic['fichtm'] = '{}{}.htm'.format(REPWORK, fic)
    dFic['ficcsv'] = '{}{}.csv'.format(REPWORK, fic)
    dFic['fickikou'] = '{}{}.csv'.format(REPDEST, fic)
    return dFic

def main(argv):
    if 'auto' in argv:
        auto = True
    else:
        auto = False
    #chargement des outils
    fic, ext = os.path.splitext(argv[0])
    fic = fic.split('/')[-1]

    tools = Tools(auto, 'livechrono')
    tools.fichiers = make_dic_fic(fic)
    tools.coureurs = tools.htmtoliste()
    
    if tools.checkCoureurs(tools.coureurs):
            tools.writeCsv(tools.coureurs, tools.fickikou)
            print(BOLD, "--> Fichier {} traité".format(tools.fichtm), RESET)
            print(BOLD, "Fichier {} pret à tranférer sur KiKourou".format(tools.fickikou), RESET)
            # sauvegarde du htm
            fic = 'mv {} {}/sv_fic_source'
            sv =  os.system(fic.format(tools.fichtm, REPWORK))
    else:
        tools.writeCsv(tools.coureurs, tools.ficcsv)
        print(BOLD, "Fichier {} pourri".format(tools.fichtm), RESET)
        for cle, valeur in tools.anos.items():
            print(BOLD, "\nAnomalie de type : ", cle, RESET)
            for ano in valeur:
                print('\t{}'.format(ano))                
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
