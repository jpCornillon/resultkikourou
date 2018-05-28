#####################################################
# A noter : 
# - en passant auto au script, la numerotation s'incremente automagiquement (élimination des doublons)
# - si pas de categorie mais des annees de naissance, il faut le preciser dans le premier champ
#      (ex: class;temps;nom;cat;annee;club)
#####################################################
import os
import sys
from datetime import datetime
import re
import subprocess
import requests   
import urllib.parse
import urllib.request                                  # sudo dnf install python3-requests
from urllib.request import urlopen, ProxyHandler       # sudo dnf install  python3-urllib
import socket
from bs4 import BeautifulSoup                          # sudo dnf install python3-beautifulsoup
import chardet                                         # detection encodage fichier (installé d'origine ???)
# classes locales
# fichier des regexp
from lib import ApplyRegex
from lib import rulesKikourou as kikourou
from lib import rulesBaseFFA  as ffa
from lib import enteteKikourou as enteteKikourou
from lib import catFFA
#
#####################################################
# globales
CSV = 'class;temps;nom;club;f1;cat\n'
BOLD = "\033[1m"
RESET = "\033[0;0m"
#
#####################################################

class MyTools(object):
    """Outils perso :
        - regex pour KiKourou
        - regex pour base ffa
    """
    def __init__(self):
        self.regKikou = ApplyRegex(kikourou.patterns)
        self.regFFA = ApplyRegex(ffa.patterns)
        self.regEntete = ApplyRegex(enteteKikourou.patterns)
        self.categories = catFFA.categories

    def choix_entete(self):
        csv = ('class', 'nom', 'temps', 'cat', 'sexe', 'club', 'prenom', 'f1')
        print('\n--> ', self.coureurs[0])
        print('--> ', self.coureurs[-1])
        choix = CSV = ''
        while not choix.isdigit():
            choix = input(BOLD + '1)class, 2)nom, 3)temps, 4)cat, 5)sexe, 6)club, 7)prenom, 8)foo, 9)ffa, 0)pas d\'entete ' + RESET)
        if choix == '': CSV = ['class', 'temps', 'nom', 'club', 'cat', 'f1']
        if '0' in choix:
            CSV = ''
            return CSV
        elif '9' in choix: 
            CSV = 'class;temps;nom;club;cat\n'
            return CSV
        else:
            for i in choix:
                CSV = CSV + '{};'.format(csv[int(i) - 1])
            return '{}{}'.format(CSV[:-1], '\n')


class Tools(MyTools):
    '''Herite de MyTools qui sont des outils personnalisés :
          - creation des attributs en fontion du dictionnaire d'options reçus
          - outils pour la gestion des fichiers
    '''
    def __init__(self, auto=False, src='livetrail'):
        super().__init__()
        self.auto = auto
        self.src = src

    @property
    def fichiers(self):
        return self.__dict__
    @fichiers.setter
    def fichiers(self, dFic):
        for key in dFic.keys():
            setattr(self, key, dFic[key])

    @property
    def options(self):
        return self.__dict__
    @options.setter
    def options(self, params):
        for key in params:
            setattr(self, key, params[key])

    def encodage_fichier(self, fic):
        #return self.fictoliste(fic)
        script = 'dos2unix {}'
        conv = os.system(script.format(fic))
        script = './conv.sh {}'
        conv = os.system(script.format(fic))
        if conv == 256 or conv == 0:
            return self.fictoliste(fic)
            #return True
        else:
            print('fichier non réencodable : plantage !!!!')
            exit(66)

    def detect_code(self, fic):
        '''retourne l'encodage du fichier'''
        rawdata = open(fic, 'rb').read()
        return chardet.detect(rawdata)['encoding']

    def fictoliste(self, fichier):
        '''lecture du fichier et retour d'une liste'''
        try:
            with open(fichier) as fic:
            #with open(fichier, encoding='iso-8859-1') as fic:
                return [self.regKikou(i) for i in fic.readlines()]
        except UnicodeDecodeError:
            raise 'problème d\'encodage'


    def htmtoliste(self, url='', data='', src='livetrail'):
        ''' 'http://www.livetrail.net/histo/traildesforts_2016/classement.php', data)
            response = urllib.request.urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, 'lxml') '''
        self.coureurs = []
        self.entete = 'class;nom;prenom;club;cat;temps'
        self.coureurs.append(self.entete)
        if self.src == 'livetrail' :
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            #html = open(self.fichtm, 'r')
            html = response.read()
            soup = BeautifulSoup(html, 'lxml')
            for cla in soup.findAll('classement'):
                for c in cla.findAll('c'):
                    if c.get('nom') == '???': 
                        nom = 'xx'
                    else:
                        nom = c.get('nom')
                    if c.get('prenom') == '???': 
                        prenom = 'xx'
                    else:
                        prenom = c.get('prenom')
                    if c.get('cat') == '':
                        print('Attention : probleme catégorie pour ', c.get('class'))
                        cat = 'SEM'
                    else:
                        cat = c.get('cat')
                    coureur = '{};{};{};{};{};{}'.format(''.join(c.get('class')), nom, prenom, c.get('club').replace('.', ''), cat.replace(' ', ''),c.get('tps'))
                    self.coureurs.append(self.sup_accent(coureur))
            return self.listetodic()
        
        elif self.src == 'livechrono':
            f = open(self.fichtm)
            soup = BeautifulSoup(f, 'lxml', from_encoding='utf8')
            for tr in soup.findAll('tr'):
                tab = tr.get_text().split('\n')
                if tab[1].isdigit():
                    coureur = '{};{};{};{};{};{}'.format(tab[1], tab[4], tab[5], tab[10].replace('/', ''), tab[7][:2]+tab[6][0], tab[8])
                    self.coureurs.append(self.sup_accent(coureur))
            return self.listetodic()

        elif self.src == 'autre':
            '''class=1 nom=2 prenom=3 sexe=4 cat=6 club=7 temps=8'''
            f = open(self.fichtm)
            soup = BeautifulSoup(f, 'lxml', from_encoding='utf8')
            for tr in soup.findAll('tr'):
                tab = tr.get_text().split('\n')
                if tab[1].isdigit():
                    self.entete = 'class;nom;prenom;club;cat;temps'
                    coureur = '{};{};{};{};{};{}'.format(tab[1], tab[2], tab[3], tab[7], self.regKikou(tab[6]) + tab[4], tab[8])
                    self.coureurs.append(self.sup_accent(coureur))
            return self.listetodic()


    def csvtoliste(self):
        '''depuis un fichier csv :
        - decodage du fichier
        - creation liste de coureur
        - retour d'une liste de coureurs'''
        a_virer =  self.encodage_fichier(self.ficcsv)
        self.coureurs =  [ self.regKikou(i) for i in a_virer ]
        if not self.coureurs[0].lower().startswith('class'):
            self.entete = self.regEntete(self.choix_entete())
            self.coureurs = self.entete.split() + self.coureurs
        if self.check_format(): 
            return self.listetodic()
        else:
            print(BOLD + '\nProbleme avec le fichier {} \
                \nCorriger le fichier et relancer \'./kikourou.py {}'.format(self.ficcsv, self.ficcsv) + RESET)
            for ano in self.anos_format: print('--> ', ano)
            exit(1)

    def pdftoliste(self):
        '''depuis un fichier csv
        - utilitaire pdftotext avec creation d_un csv provisoire'''
        fic = "pdftotext -layout {} - |sed -e 's/^L//' -e 's/^ *//'|grep '^ *[0-9][0-9]*' \
                                      |sed -r 's/  +/;/g; s/  //g'|sed '/^[0-9]$/d'|sed -e 'y/éèêëàçùâîïÉÈÇÀÙ/eeeeacuaiiEECAU/' -e 's/°//'"
        proc = subprocess.Popen(fic.format(self.ficpdf), stdout=subprocess.PIPE, shell=True)
        datas1 = [coureur.decode().strip() for coureur in proc.stdout.readlines()]
        # liste des coureurs (avec application des regexp Kikourou) 
        self.coureurs = [ self.regKikou(c) for c in datas1 if 'Page' not in c ]
        # liste des coureurs avec entete
        self.entete = self.regEntete(self.choix_entete())
        self.coureurs = self.entete.split() + self.coureurs
        a_virer = self.entete.split() + self.coureurs
        if self.check_format(): 
            return self.listetodic()
        else:
            print(BOLD + '\nProbleme avec le fichier {} \
                \nCorriger le fichier {} \
                \nEnsuite, relancer \'./kikourou.py {}'.format(self.ficpdf, self.ficcsv, self.ficcsv) + RESET)
            for ano in self.anos_format: print('--> ', ano)
            with open(self.ficcsv, 'w') as f:
                for c in self.coureurs:
                    f.write('{}\n'.format(c))
            exit(1)

    def check_format(self):
        ok = True
        self.anos_format = []
        entete = self.coureurs[0].split(';')
        # gestion des coureurs avec ou sans club
        avec_club = [self.regEntete(i.lower()) for i in entete]
        sans_club = [ i for i in avec_club if i != 'club']
        for coureur in self.coureurs[1:]:
            coureur = self.regKikou(coureur)
            ligne = coureur.split(';')
            if len(ligne) == len(avec_club):
                dco = dict(zip(avec_club, ligne))
            elif len(ligne) == len(sans_club):
                dco = dict(zip(sans_club, ligne))
            else:
                ok = False
                self.anos_format.append(ligne)
        if ok:
            return True
        else:
            return False

    def listetodic(self):
        ano = False
        position = 0
        dic = []
        entete = self.coureurs[0].split(';')
        # gestion des coureurs avec ou sans club
        avec_club = [self.regEntete(i.lower()) for i in entete]
        sans_club = [ i for i in avec_club if i != 'club']
        for coureur in self.coureurs[1:]:
            position +=1
            ligne = self.regKikou(coureur).split(';')
            if len(ligne) == len(avec_club):
                dco = dict(zip(avec_club, ligne))
            elif len(ligne) == len(sans_club):
                dco = dict(zip(sans_club, ligne))
            else:
                print('Probleme: ', ligne)
            # print(dco)
            if self.auto:
                dco['class'] = str(position)
            if dco['class'].lower() not in ['dnf', 'ur']:
                dic.append(self.formatdic(dco))
        return dic
            # try:
            #     if dco['class'].lower() not in ['dnf', 'ur']:
            #         dic.append(self.formatdic(dco))
            # except:
            #     print(dco)
            #     ano = True
        #if ano:
        #    exit(1)
        #else:
        #    return dic

    def formatdic(self, dco):
        '''Formatage du dico'''
        # print(dco)

        # pas de <cat> mais une <annee>
        if 'annee' in dco.keys() and not 'cat' in dco.keys():
            age = datetime.today().year - int(dco['annee'])
            for i in self.categories.keys():
                if age in self.categories[i]:
                    dco['cat'] = i
        # <cat>
        if len(dco['cat']) == 3:
            a_virer = dco['cat']
            dco['sexe'] = a_virer[2]
            dco['cat'] = a_virer[0:2]
        dco['cat'] = dco['cat'].upper()
        # </cat>
        
        # <sexe>
        if 'sexe' not in dco.keys():
            dco['sexe'] = ''
        if (dco['sexe'] == '' and (dco['cat'][-1] == 'H' or dco['cat'][-1] == 'M')) or dco['sexe'] == 'H':
            dco['sexe'] = 'M'
        elif dco['sexe'] == '' and (dco['cat'][-1] == 'F' or dco['cat'][-1] == 'F'):
            dco['sexe'] = 'F'
        # </sexe>

        # <temps>
        if len(dco['temps']) == 5:
            dco['temps'] = '0:{}'.format(dco['temps'])
        if re.search('\.[0-9][0-9]$', dco['temps']):  # suppression des dixiemes de seconde
            dco['temps'] = re.sub('\.[0-9][0-9]$', '', dco['temps'])
        if len(dco['temps']) > 8:
            dco['temps'] = dco['temps'][:8]
        dco['temps'] = self.format_temps(dco['temps'])
        # <temps>

        # <club>
        if 'club' not in dco.keys():
            dco['club'] = ''
        else:
            dco['club'] = dco['club'].replace('.', '')
        # </club>
        return dco
    
    def sup_accent(self, ligne):
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

    def format_temps(self, t):
        '''complete les champs du temps avec des 0 si necessaire'''
        # a_virer =  ':'.join([ '{:02d}'.format(int(i)) for i in t.split(':')])
        a_virer = [ i.zfill(2) for i in t.split(':') ]
        return ':'.join(a_virer)

    def writeCsv(self, coureurs, fic):
        '''Le csv est créé : 
           - soit avec self.fickikou si tout bon
           - soit avec self.ficcsv pour correction des anomalies'''
        #with open(self.fickikou, 'w')as out:
        with open(fic, 'w')as out:
            out.write('class;temps;nom;cat;sexe;club\n')
            #out.write(self.entete)
            for c in coureurs:
                if 'prenom' in c.keys():
                    ligne = u'{};{};{} {};{};{};{};\n'.format(c['class'], c['temps'], c['nom'], c['prenom'], c['cat'][0:2], c['sexe'], c['club'].strip())
                else:
                    ligne = u'{};{};{};{};{};{};\n'.format(c['class'], c['temps'], c['nom'], c['cat'][0:2], c['sexe'], c['club'].strip())
                out.write(ligne)
        out.close()

    def checkCoureurs(self, coureurs):
        '''verification du fichier produit et creation d'un tableau des anomalies'''
        retour = []
        cat = ['SE', 'V1', 'V2', 'V3', 'V4', 'V5', 'JU',
               'CA', 'ES', 'MI', 'BE', 'PO', 'EA', 'HD', 'HA']
        sex = ['M', 'F']
        self.anos = {}
        i = 0
        for c in coureurs:
            out = ''
            for k,v in c.items():
                out = out + '<{}={}> '.format(k,v)
            # <classement>
            i += 1
            if int(c['class']) != i:
                self.anos.setdefault('sequencement', []).append('classement attendu {}, trouve {} : {}'.format(i, int(c['class']), out))
            # </classement>

            # <temps>
            try:
                datetime.strptime(c['temps'], '%H:%M:%S')
            except:
                self.anos.setdefault('temps', []).append('format non correct <{}> : {}'.format(c['temps'], out))
            # </temps>
            
            # <nom, prenom,club>
            if '.' in c['nom']:
                self.anos.setdefault('nom', []).append('caractere <.> interdit dans le nom <{}> : {}'.format(c['nom'], out))
            if 'prenom' in c.keys() and '.' in c['prenom']:
                self.anos.setdefault('prenom', []).append('caractere <.> interdit dans le prenom <{}> : {}'.format(c['prenom'], out))
            if '.' in c['club']:
                self.anos.setdefault('club', []).append('caractere <.> interdit dans le club <{}> : {}'.format(c['club'], out))
            # </nom, prenom,club>
            
            # <cat>
            if len(c['cat']) != 2:
                self.anos.setdefault('cat', []).append('longeur de catégorie non correcte : {}'.format(out))
                #self.anos.setdefault('cat', []).append('longeur de catégorie non correcte <{}> : {}'.format(c['cat'], out))
            if c['cat'] not in cat:
                self.anos.setdefault('cat', []).append('catégorie non reconnue : {}'.format(out))
                #self.anos.setdefault('cat', []).append('catégorie non reconnue <{}> : {}'.format(c['cat'], out))
            # </cat>
            
            # <sexe>
            if c['sexe'] not in ['M', 'F']:
                self.anos.setdefault('sexe', []).append('attendu <M> ou <F> , trouve {} : dans {}'.format(c['sexe'], out))
            # </sexe>
            # 
        # sortie de la methode
        if len(self.anos.items()) == 0:
            return True
        else:
            return False
