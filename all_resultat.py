#!/usr/bin/python3
# -*- coding: utf8
#
########"""""""#############################################
# TODO : 
# - sed a faire sur la ville pour sup accent, cedile, ect...
# - ne fonctionne pas sur les petits fichiers (<200 ? )
# - remettre le rm a la fin de ffaClub.py 
############################################################
#
import os
import socket
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
FICDIR = '{}/dropbox/kikourou/'.format(os.environ['HOME'])
BOLD = "\033[1m"
RESET = "\033[0;0m"
#
#####################################################

def urlopenPaulo(url):
    '''si je suis au taf, je passe par le proxy'''
    ip = socket.gethostbyname(socket.getfqdn())
    # mon, ip taf contient 227
    if '227' in ip:
        proxies = {'http': 'squid:8080'}
        html = requests.get(url, proxies=proxies).text
    else:
        html = urlopen(url)
    return html

def lec_html():
    '''lecture/extraction des liens de la page résultat de chez kiourou'''
    URL = FICDIR+'/fichiers/source/kikourou_files/resultats.htm'
    courses = []
    html = open(URL, 'r')
    soup = BeautifulSoup(html)
    #soup = BeautifulSoup(html, 'lxml')
    for li in soup.findAll('li'):
        lien = li.find('a')
        courses.append(lien.get('href'))
    return courses

def lec_specCourse(course):
    ''' recup infos chez kikourou'''
    url = 'http://www.kikourou.net{}#ongletinfo'.format(course)
    print(course)
    print(url)
    #html = open(URL, 'r')
    #soup = BeautifulSoup(html)
    html = urlopenPaulo(url)
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', { 'class' : 'contenu-texte'})
    lieuCourse = div.find('a').text
    datas = [ data.previous_sibling for data in div.findAll('br') if '\n' not in data]
    dateCourse = trtDate(datas[1])
    depCourse = trtDepartement(datas[2].lstrip())
    kmCourse = datas[3]
    return [ dateCourse, lieuCourse, depCourse ]

def trtDate(dat):
    datas = dat.split()
    jj = datas[1]
    mois = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre' ]
    dicMois = dict(zip(mois,[i for i in range(1, 13)] ))
    mm = dicMois[datas[2].replace('û','u').replace('ê', 'e').replace('é', 'e')]
    aa = datas[3]
    #return ({}, {}, {}).format(jj, mm, aa)
    return (jj, mm, aa)

def trtDepartement(dpt):
    (r';(V[1-5])(-H);',  r';\1M;', True)
    dept=re.sub(r'\(([0-9][0-9]).*$', r'\1', dpt, flags=re.IGNORECASE)
    return dept


def consult_calendrierFFA(datas):
    URL = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison={}&frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement={}&frmeprrch=&frmclub=&frmdate_j1={}&frmdate_m1={}&frmdate_a1={}&frmdate_j2={}&frmdate_m2={}&frmdate_a2={}'
    jj, mm, aa = datas[0]
    lieuK = datas[1].lower().replace(' ', '').replace('-', '')
    lieuK = sup_accent(lieuK)
    # departement sur 3 chiffres avec un 0 (sauf pour les dom)
    dept = '0{}'.format(datas[2]) if len(datas[2]) == 2 else datas[2]
    url = URL.format(aa, dept, jj, mm, aa, jj, mm, aa)
    html = urlopenPaulo(url)
    sleep(2)
    course = courses = []
    soup = BeautifulSoup(html, 'lxml')
    for tr in soup.findAll('tr'):
        num = ''
        course = []
        for td in tr.findAll('td', class_=["datasCMP0", "datasCMP1"]):
            if td.text != '':
                course.append(td.text)
            if td.a:
                num = td.a.get('href')[-6:]
                course.append(num)
                participants = re.sub(r'(^.*- )([0-9]+)(.*)', r'\2', td.a.get('title'))
                course.append(participants)
                num = u'%s (%s coureurs)' % (num, participants)
        if len(course) > 0:
            lieuF = course[5].lower().replace(' ', '').replace('-', '')
            lieuF = sup_accent(lieuF)
            print('kikourou : ', lieuK, '- ffa : ', lieuF)
            if lieuK == lieuF:
                courses.append([ course[0], course[2], course[3], course[4], course[5], course[7] ])
    if len(courses) > 0:
        return courses
    else:
        return ''

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

def consult_courseFFA(datas):
    #dicCourse = " aa/mm, nom course, num course, nb participants, lieu, departement"
    nomcourse = datas[1]
    numcourse = datas[2]
    participants = datas[3]
    participants=int(participants)
    nb_page = int(int(participants) / 200) + 1
    URL = 'http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={}&frmposition={}'
    # pour trouver les epreuves d'une course, on se positionne directement sur le 3ème bouton select
    # URL course pour recherche epreuve
    URL_COURSE = 'http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={}'
    epreuves=[]
    #numcourse='197063'
    html = urlopenPaulo(URL_COURSE.format(numcourse))
    soup = BeautifulSoup(html, 'lxml')
    #selects =  soup.findAll('select', class_=["barSelect"])[2]
    selects =  soup.findAll('select', class_=["barSelect"])
    if len(selects) == 6:
        select = selects[2]
    elif len(selects) == 4:
        select = selects[1]
    else:
        print('Probleme avec le "select" de la course numéro : {}'.format(numcourse))
    for option in select.findAll('option'):
        if option['value'] != '':
            epreuve = option.text.replace('\xa0', '')
            epreuve = epreuve.replace(' ', '')
            epreuve = epreuve.replace('<', '')
            epreuve = epreuve.replace('>', '')
            epreuves.append([option['value'], epreuve])
    # URL d'une epreuve page 0 et suivante : http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition=179109&frmepreuve=10+Km+Route+TC&frmposition=1
    URL_EPREUVE ='http://bases.athle.com/asp.net/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={}&frmepreuve={}&frmposition={}'
    coureur = coureurs = []
    course = {}
    for epreuve in epreuves:
        html = urlopenPaulo(URL_EPREUVE.format(numcourse, epreuve[0], 0))
        soup = BeautifulSoup(html, 'lxml')
        try:
            participants = soup.find('td', class_=["barCount"]).text
            participants = re.sub(r'(^[0-9]+)(.*$)', r'\1', participants)
            nb_page = int(int(participants) / 200) + 1
        except:
            nb_page = 1
        print('Course : {} - Epreuve : {} ({} participants)'.format(nomcourse, epreuve[1], participants))
        for i in range(0, nb_page):
            #on charge les coureurs de l'epreuve
            url = URL_EPREUVE.format(numcourse, epreuve[0], i)
            print(' --> page : {}'.format(i))
            html = urlopenPaulo(URL_EPREUVE.format(numcourse, epreuve[0], i))
            soup = BeautifulSoup(html, 'lxml')
            for tr in soup.findAll('tr'):
                coureur = [ td.text for td in tr.findAll('td', class_=["datas0", "datas1"]) if '\xa0' not in td]
                if coureur != []: coureurs.append(';'.join(coureur))
        course[epreuve[1]] = coureurs
        coureurs = []
        sleep(2)
    return course

def listetofic(fic, epreuve, liste):
    '''ecriture fichier depuis une liste'''
    r = ApplyRegex(kikourou.patterns)
    #fichier = '/home/paulo/dropbox/kikourou/fichiers/source/{}.html'.format(fic)
    fichier = '{}/fichiers/source/{}_{}.txt'.format(FICDIR, fic, epreuve)
    entete = 'class;temps;nom;club;cat\n'
    try:
        with open(fichier, 'w') as fic:
            fic.write(entete)
            for l in liste:
                l = '{}\n'.format(r(l))
                fic.write(l)
            fic.close
        return True
    except:
        return False

def main():
    f = ApplyRegex(FFA.patterns)
    link_courses_kikou = lec_html()
    #for course in link_courses_kikou: print(course)
    #print(link_courses_kikou[0])
    #courses = ['/calendrier/course-100420-trail_semnoz_tour_-_45_km-2016.html', '/calendrier/course-102736-le_cul_d_enfer_-_21_km-2016.html']
    #courses = ['/calendrier/course-100420-trail_semnoz_tour_-_45_km-2016.html']
    #courses = ['/calendrier/course-106555-les_foulees_terre_d_envol_-_semi-2016.html']
    dicCourse = {}
    for course in link_courses_kikou:
        '''link_courses_kikou : liste des courses chez kikourou'''
        fic, ext = os.path.splitext(course)
        fic = fic.split('/')[-1]
        #print(fic, ' - ', ext)

        # obtention des infos de la course chez KiKourou
        # retour de fonction lec_specCourse : datas = [ (jj, mm, aa), lieuCourse, depCourse ]
        datas = lec_specCourse(course)
        #print(datas)

        # obtention des infos de la course à la FFA
        # retour de la fonction consult_calendrierFFA() : coursesFFA = [ [date, nom course, num course, nb coureurs, lieu, dept] , [...]  ]
        coursesFFA = consult_calendrierFFA(datas)
        if not coursesFFA:
            print(BOLD + 'course {} non trouvée sur base athlé.'.format(fic) + RESET)
            #print()
            continue
        for courseFFA in coursesFFA:
            if len(courseFFA) > 0:
                print('Traitement de la course : {} ({} participants)'.format(courseFFA[1], courseFFA[3]))
                # obtention liste coureurs depuis base FFA
                dicCourse[fic] = consult_courseFFA(courseFFA)
                for epreuve in dicCourse[fic].keys():
                    coureurs = [f(coureur) for coureur in dicCourse[fic][epreuve]]
                    if listetofic(fic, epreuve, coureurs): 
                        print('  ---> fichiers/source/{}_{}.txt'.format(fic, epreuve))
                        script = './ffaClub.py fichiers/source/{}_{}.txt'
                        ficdef = os.system(script.format(fic, epreuve))
                    else:
                        print('----------------------')
                        print('Course : {}  à {} ({})'.format(courseFFA[1], courseFFA[4], courseFFA[5], courseFFA[0]))
                        print(BOLD + '    ---> probleme !!!!' + RESET)
            else:
                print(BOLD + 'course {} non trouvée sur base athlé.'.format(fic) + RESET)
                print()
#
#####################################################
#
if __name__ == '__main__':
    main()
#
#####################################################
