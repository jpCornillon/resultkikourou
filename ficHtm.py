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
REPWORK = '{}{}'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/source/')
REPDEST = '{}{}'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/csv/')
BOLD = "\033[1m"
RESET = "\033[0;0m"
# import pdb; pdb.set_trace()
#######################################################################################
#


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

    tools = Tools(auto, 'autre')
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
