#!/usr/bin/python3
# -*- coding: utf8
#
#####################################################
#
import os
import sys
import argparse
import re
import requests                                        # sudo dnf install python3-requests
from urllib.request import urlopen, ProxyHandler       # sudo dnf install  python3-urllib
import socket
from bs4 import BeautifulSoup                          # sudo dnf install python3-beautifulsoup
import chardet                                         # detection encodage fichier (installé d'origine ???)
from time import sleep
# classes locales
# fichier des regexp
from lib import ApplyRegex
from lib import rulesKikourou as kikourou
from lib import rulesBaseFFA  as ffa
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
#
#####################################################
# classes
class Factory(object):
    """docstring for Factory"""
    def __init__(self):
        super().__init__()
        print('objets : ', self.objets)

    @staticmethod
    def get_factory(which):
        if which == 'pdf':
            return PdfFactory()
        elif which == 'all':
            return AllFactory()
        elif which == 'csv':
            return CsvFactory()
        elif which == 'htm':
            return HtmFactory()
        elif which == 'txt':
            return TxtFactory()
        elif which == 'xlsx':
            return XlsxFactory()
        elif which == 'course':
            return CourseFactory()
        else:
            return CalendrierFactory()

    def create_file(self):
        raise NotImplementedError()


class AllFactory(object):
    def genClass(self, options):
        return All()


class CalendrierFactory(object):
    def genClass(self, options):
        return Calendrier()


class PdfFactory(object):
    def genClass(self, options):
        return Pdf()


class CsvFactory(object):
    def genClass(self, options):
        return Csv()


class HtmFactory(object):
    def genClass(self, options):
        return Htm()


class TxtFactory(object):
    def genClass(self):
        return Txt()


class XlsxFactory(object):
    def genClass(self, options):
        return Xlsx()


class CourseFactory(object):
    def genClass(self, options):
        return Course()


class All(Tools):
    """Traitement de tous les fichiers <ext> du repertoire:
         - on parcours le repertoire et on extrait les noms de fichiers
         - creation d'un dico avec nom, extensions
    """

    def start(self):
        if self.ext == '*':
            print('traitement de tous les fichiers')
        else:
            print('{}Traitement des fichiers {} :{}'.format(BOLD, self.ext, RESET))
        # self.lst_fic = glob('fichiers/source/*{}'.format(self.ext))
        self.lst_fic = [fic for fic in os.listdir('fichiers/source/') if fic.endswith('.{}'.format(self.ext))]
        for fic in self.lst_fic:
            print('{}    ---> {}{}'.format(BOLD, fic, RESET))
            f = Factory.get_factory(self.ext)
            c = f.genClass()
            c.options = self.params(fic)
            c.start()

    def params(self, fic):
        fic, ext = os.path.splitext(self.lst_fic[0])
        fic = fic.split('/')[-1]
        _dic = {}
        _dic['ficpdf'] = '{}{}.pdf'.format(FICDIR, fic)
        _dic['ficcsv'] = '{}{}.csv'.format(FICDIR, fic)
        _dic['fictxt'] = '{}{}.txt'.format(FICDIR, fic)
        _dic['fichtm'] = '{}{}.htm'.format(FICDIR, fic)
        return _dic


class Pdf(Tools):
    """Gestion d'un fichier pdf :
        - on le convertit avec pdftotext
        - creation d'un fichier csv (avec application des regex)
    """
    def start(self):
        self.coureurs = self.pdftoliste()
        if self.checkCoureurs(self.coureurs):
            self.writeCsv(self.coureurs, self.fickikou)
            print(BOLD, "  <{}> : correct".format(self.ficpdf), RESET)
            print(BOLD, "  <{}> : a tranférer sur KiKourou".format(self.fickikou), RESET)
            # sauvegarde des fichiers de source vers sv_fic_source
            fic = 'mv {}* {}sv_fic_source'.format(self.ficcsv[:-4], REPWORK)
            sv =  os.system(fic)
        else:
            print(BOLD, '\nFichier {} pourri'.format(self.ficpdf), RESET)
            print(BOLD, 'Modifier le fic {} et relancer'.format(self.ficcsv), RESET)
            self.writeCsv(self.coureurs, self.ficcsv)
            for cle, valeur in self.anos.items():
                print(BOLD, "\nAnomalie de type : ", cle, RESET)
                for ano in valeur:
                    print('   {}'.format(ano))        

        #if self.pdftocsv():
        #    print('- Fichier {} traité.\n- Fichier {} créé.'.format(self.ficpdf, self.ficcsv))
        #    if self.encodage_fichier(self.ficcsv) and self.csvtotxt():
        #        print('- Fichier {} créé.'.format(self.fictxt))
        #        self.csvdef()
        #    return True


class Xlsx(Tools):
    """Gestion d'un fichier xlsx :
        - utilisation du script xls2csv.py
        - chargement/formatage des coureurs en table
        - ecriture fichier si OK"""
    def start(self):
        self.coureurs = self.xlsxtoliste()
        if self.checkCoureurs(self.coureurs):
            self.writeCsv(self.coureurs, self.fickikou)
            print(BOLD, "  <{}> : correct".format(self.ficxlsx), RESET)
            print(BOLD, "  <{}> : a tranférer sur KiKourou".format(self.fickikou), RESET)
            # sauvegarde des fichiers de source vers sv_fic_source
            fic = 'mv {}* {}sv_fic_source'.format(self.ficxlsx[:-4], REPWORK)
            sv =  os.system(fic)
        else:
            print(BOLD, 'Fichier {} pourri'.format(self.ficxlsx), RESET)
            self.writeCsv(self.coureurs, self.ficcsv)
            for cle, valeur in self.anos.items():
                print(BOLD, "\nAnomalie de type : ", cle, RESET)
                for ano in valeur:
                    print('   {}'.format(ano))        
                    print('   {}'.format(ano))       

class Csv(Tools):
    """Gestion d'un fichier csv :
        - lecture du csv
        - chargement/formatage des coureurs en table
        - ecriture fichier si OK"""
    def start(self):
        self.coureurs = self.csvtoliste()
        if self.checkCoureurs(self.coureurs):
            self.writeCsv(self.coureurs, self.fickikou)
            print(BOLD, "  <{}> : correct".format(self.ficcsv), RESET)
            print(BOLD, "  <{}> : a tranférer sur KiKourou".format(self.fickikou), RESET)
            # sauvegarde des fichiers de source vers sv_fic_source
            fic = 'mv {}* {}sv_fic_source'.format(self.ficcsv[:-4], REPWORK)
            sv =  os.system(fic)
        else:
            print(BOLD, 'Fichier {} pourri'.format(self.ficcsv), RESET)
            self.writeCsv(self.coureurs, self.ficcsv)
            for cle, valeur in self.anos.items():
                print(BOLD, "\nAnomalie de type : ", cle, RESET)
                for ano in valeur:
                    print('   {}'.format(ano))        
                    print('   {}'.format(ano))        


class Htm(Tools):
    """Gestion d'un fichier htm :
        - lecture fichier html
        - creation d'un fichier csv (avec application des regex)
        - enfin, creation d'un fichier txt
    """
    def start(self):
        if self.encodage_fichier(self.fichtm) and self.htmtocsv():
            print('- Fichier {} traité.\n- Fichier {} créé.'.format(self.fichtm, self.ficcsv))
            if self.csvtotxt():
                print('- Fichier {} créé.'.format(self.fictxt))
        return True


class Txt(Tools):
    """on passe d'un fichier txt a un fichier csv dans Fichiers/csv :
    - lecture txt : fictoliste
    - creation dictionnaire
    - ecriture fichier csv si aucune anomalie
    """
    def start(self):
        print (self.options)
        return 'Objet Txt - Fichier : {}'.format(self.fichier)


class Course(Tools):
    """a partir du numero de course :
        - calcul du nombre de participants
        - calcul du nombre de page à extraire
        - si option -f, ecriture d'un fichier
    """
    def start(self):
        for epreuve in self.liste_epreuves():
            # url = 'http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={}&frmepreuve={}'
            url = 'http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={}&frmepreuve={}&frmposition={}'
            suite = True
            self.coureurs = []
            self.url_epreuve = url.format(self.numcourse, epreuve.lower(), 0)
            self.participants = self.nb_participants()
            self.nb_page = int(self.participants / 250) + 1
            self.fic_epreuve = '{}_{}.csv'.format(self.ficcsv[:-4], epreuve.lower().replace('+', '_'))
            print(BOLD, '\nTraitement epreuve {} :'.format(self.fic_epreuve.split('/')[-1]), RESET)
            for page in range(0, self.nb_page):
                # sleep(2)
                # print('page {}/{}'.format( page, self.nb_page))
                self.url_epreuve = url.format(self.numcourse, epreuve.lower(), page)
                if self.nb_participants() > 0:
                    self.coureurs += self.lec_html()
                else:
                    print('- aucun participant trouvé pour la course n° {}'.format(self.numcourse))
            # tentative pour ne garder que le bon nombre de participants (probleme de la derniere page)
            self.coureurs = self.coureurs[ :self.participants +1 ]
            self.entete = 'class;temps;nom;club;cat'
            self.coureurs = [self.regFFA(';'.join(coureur)) for coureur in self.coureurs]
            self.coureurs = self.entete.split() + self.coureurs
            if self.check_format(): 
                self.coureurs =  self.listetodic()
            else:
                with open(self.fic_epreuve, 'w')as out:
                    for c in self.coureurs:
                        out.write('{}\n'.format(c))
                print(BOLD + ' - probleme avec le fichier {} \
                              \n - Corriger le fichier et relancer \'./kikourou.py {}'.format(self.fic_epreuve, self.fic_epreuve) + RESET)
                for ano in self.anos_format:
                    print('--> ', ano)
                    print('')
                suite = False
                ###
            if suite:
                if self.checkCoureurs(self.coureurs):
                    dest = self.fic_epreuve.replace('/source/', '/csv/')
                    print(BOLD, ' - <{}> : correct'.format(self.fic_epreuve), RESET)
                    print(BOLD, ' - <{}> : a tranférer sur KiKourou'.format(dest), RESET)
                    self.writeCsv(self.coureurs, dest)
                else:
                    print(BOLD, ' - fichier {} pourri'.format(self.fic_epreuve), RESET)
                    self.writeCsv(self.coureurs, self.fic_epreuve)
                    for cle, valeur in self.anos.items():
                        print(BOLD, ' - anomalie de type : ', cle, RESET)
                        for ano in valeur:
                            print('   {}'.format(ano))        

    def nb_participants(self):
        # html = urlopen('file:///home/paulo/dropbox/kikourou/testCourse0.htm')
        html = urlopen(self.url_epreuve)
        soup = BeautifulSoup(html, 'lxml')
        nb = [i for i in soup.find(True, {'class': ['barCount']})]
        return int(re.sub(r'([0-9]+)( .*)', r'\1', ''.join(nb)))

    def lec_html(self):
        coureur  = []
        coureurs = []
        html = urlopen(self.url_epreuve)
        soup = BeautifulSoup(html, 'lxml')
        for tr in soup.findAll('tr'):
            coureur = [ td.text for td in tr.findAll('td', class_=["datas0", "datas1"]) if '\xa0' not in td]
            if coureur != []:
                coureurs.append(coureur)
        return coureurs

    def liste_epreuves(self):
        URL = 'http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={}'
        html = urlopen(URL.format(self.numcourse))
        soup = BeautifulSoup(html, 'lxml')
        td = [ td for td in soup.findAll('td',{ "class" : "barInputs" }) ]
        options = td[3].findAll('option')
        ### si une seule épreuve à rechercher : 
        ### http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition=192341&frmepreuve=13+km
        ### return ['13+km']
        return [ option.get('value') for option in options if option.get('value') ]

    def display(self):
        retour = ''
        for i in self.coureurs:
            if len(i) > 7:
                if retour == '':
                    retour = u"class: %-5s  -  Nom: %-30s  -  Temps: %-12s" % (i[0], i[2], i[1])
                else:
                    retour += u"\nclass: %-5s  -  Nom: %-30s  -  Temps: %-12s" % (i[0], i[2], i[1])
        return retour


class Calendrier(Tools):
    """docstring for Calendrier"""

    def nb_jour_mois(self):
        '''renvoi le nombre de jour du mois'''
        nj = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[self.mois]
        if self.mois == 2 and ((self.annee % 4 == 0 and self.annee % 100 != 0) or self.annee % 400 == 0):
            return nj + 1
        return nj

    def start(self):
        self.liste_courses = self.consult_calendrier()
        if len(self.liste_courses) > 0:
            print(self.resultat())
        else:
            print('Aucune compétition trouvée avec ces paramètres:\n- année : {}  mois : {}\n- departement : {}'.format(self.annee, self.mois, self.dept))

    def consult_calendrier(self):
        URL = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison={}&frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement={}&frmeprrch=&frmclub=&frmdate_j1={}&frmdate_m1={}&frmdate_a1={}&frmdate_j2={}&frmdate_m2={}&frmdate_a2={}'
        self.deb = 1
        url = URL.format(self.annee, self.dept, self.deb, self.mois, self.annee, self.nb_jour_mois(), self.mois, self.annee)
        ip = socket.gethostbyname(socket.getfqdn())
        html = urlopen(url)
        course = courses = []
        soup = BeautifulSoup(html, 'lxml')
        for tr in soup.findAll('tr'):
            course = []
            num = ''
            for td in tr.findAll('td', class_=["datasCMP0", "datasCMP1"]):
                if td.text != '':
                    course.append(td.text)
                if td.a:
                    num = td.a.get('href')[-6:]
                    participants = re.sub(r'(^.*- )([0-9]+)(.*)', r'\2', td.a.get('title'))
                    num = u'%s (%s coureurs)' % (num, participants)
            course.append(num)
            if len(course) > 6:
                courses.append(course)
        return courses

    def resultat(self):
        retour = ''
        for i in self.liste_courses:
            if len(i) > 8:
                if retour == '':
                    retour = u"date: %-9s  -  Course: %-45s  -  Numero : %-25s  -  Lieu: %-30s  -  Departement: %3s" % (i[0], i[2], i[-1], i[3], i[5])
                else:
                    retour += u"\ndate: %-9s  -  Course: %-45s  -  Numero : %-25s  -  Lieu: %-30s  -  Departement: %3s" % (i[0], i[2], i[-1], i[3], i[5])
        return retour


#
# fonctions
def opt(argv):
    '''dictionnaire qui sera passé à la création des objets de la fabrique'''
    parser = argparse.ArgumentParser(prog='./parser.py', usage='%(prog)s [options]', description='Generation csv...')
    #parser.add_argument('fic', nargs='*', default='')
    subparsers = parser.add_subparsers(help='sub-command help')
    # gestion du numerotage automagique
    auto = False
    if 'auto' in argv:
        auto = True
        argv.remove('auto')

    #uniquement un nom de fichier
    if len(argv) == 1:
        #on recupere uniquement le nom du fichier
        dic = {}
        fic, _ = os.path.splitext(argv[0])
        fic = fic.split('/')[-1]
        ext = argv[0].split('.')[-1]
        dic['which']    = '{}'.format(ext)
        dic['ficpdf']   = '{}{}.pdf'.format(REPWORK, fic)
        dic['ficcsv']   = '{}{}.csv'.format(REPWORK, fic)
        dic['ficxlsx']  = '{}{}.xlsx'.format(REPWORK, fic)
        dic['fictxt']   = '{}{}.txt'.format(REPWORK, fic)
        dic['fichtm']   = '{}{}.htm'.format(REPWORK, fic)
        dic['fickikou'] = '{}{}.csv'.format(REPDEST, fic)
        if auto:
            dic['auto'] = True
        return dic
    elif len(argv) > 1:
        # recherche dans le calendrier
        parser_a = subparsers.add_parser('calendrier', help='Recherche dans le calendrier Base Athlé')
        parser_a.set_defaults(which='calendrier')
        parser_a.add_argument("-d", "--dept", action="store", dest="dept", default='069', help="Departement a rechercher")
        parser_a.add_argument("-m", "--mois", action="store", dest="mois", default='6', type=int, help="Mois recherché en numerique")
        parser_a.add_argument("-a", "--annee", action="store", dest="annee", default='2017', type=int, help="Année recherchée")
    
        # recherche resultat d'une course
        parser_b = subparsers.add_parser('course', help='Consultation d\'une course')
        parser_b.set_defaults(which='course')
        parser_b.add_argument("-n", "--num", action="store", dest="numcourse", help="Course a rechercher")
        parser_b.add_argument("-f", "--fichier", action="store", dest="fichier", default=None, help="Nom du fichier en sortie")
        #traitage des options   
        options = parser.parse_args()
        dic = dict(options._get_kwargs())
        if (dic['which'] == 'course' and not dic['fichier']) or (dic['which'] == 'calendrier') or (dic['which'] == 'all'):
            dic['ficcsv'] = dic['fictxt'] = dic['fichtm'] = None
        else:
            fic, ext = os.path.splitext(dic['fichier'])
            fic = fic.split('/')[-1]
            dic['ficpdf'] = '{}{}.pdf'.format(REPWORK, fic)
            dic['fictxt'] = '{}{}.txt'.format(REPWORK, fic)
            dic['fichtm'] = '{}{}.htm'.format(REPWORK, fic)
            dic['ficcsv'] = '{}{}.csv'.format(REPWORK, fic)
            dic['fickikou'] = '{}{}.csv'.format(REPDEST, fic)
        return dic
    else:
        parser.error('./parser.py -h [--help] pour obtenir la liste des options')
#
#####################################################
#


def main(argv):
    #dictionnaire des options
    options = opt(argv)
    
    #utilisation de la fabrique : retourne un objet en fonction de l'extension du fichier transmis
    f = Factory.get_factory(options['which'])
    
    #creation/lancement objet
    c = f.genClass(options)
    c.options = options
    c.start()
#
#####################################################
#
if __name__ == '__main__':
    main(sys.argv[1:])
#
#####################################################
