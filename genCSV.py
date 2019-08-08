#!/usr/bin/python3
# -*- coding: utf8
#
# mettre une ligne d'entete
# pas de champ avec des ?
# pas de champ avec des .
# pas de champ avec espaces
# mettre des XXX si rien n'est connu
# si club vide : mettre un blanc a la place d'un tiret
#
# CSV='class;temps;nom;cat;sexe;club'
#
#
from sys import argv
import os.path
from datetime import datetime
import re
from lib import ApplyRegex
from lib import rulesKikourou as kikourou
from lib import enteteKikourou as entete
#
# format attendu du csv = class;temps;nom;cat;sexe;club
# globales
BOLD = "\033[1m"
RESET = "\033[0;0m"
#FICDIR = '{}{}'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/source/')
#
# ATTENTION : il faut adapter TXT en fonction du fichier d entree
# TXT_AVEC_CLUB= ['class', 'nom', 'club', 'cat', 'temps']
# TXT_SANS_CLUB= [ txt for txt in TXT_AVEC_CLUB if txt != 'club']
#
r = ApplyRegex(entete.patterns)

def lecFic(FIC, numAuto=False):
    ligne = ''
    position = 0
    coureurs = []
    premier = correct = True
    with open(FIC) as fic:
        ENTETES = fic.readline().split(';')
        TXT_AVEC_CLUB = [r(i.lower()) for i in ENTETES]
        TXT_SANS_CLUB = [txt for txt in TXT_AVEC_CLUB if txt != 'club']
        lignes = fic.readlines()
        suite = True
    for ligne in lignes:
        dico = {}
        tab = [i.rstrip() for i in ligne.split(';')]
        position += 1
        if len(tab) == len(TXT_AVEC_CLUB):
            correct = True
            dico = dict(zip(TXT_AVEC_CLUB, tab))
            if numAuto:
                dico['class'] = position
        elif len(tab) == len(TXT_SANS_CLUB):
            correct = True
            dico = dict(zip(TXT_SANS_CLUB, tab))
            if numAuto:
                dico['class'] = position
        else:
            correct = suite = False
            if premier:
                print('Liste des enregistrements non reconnu : ')
                premier = False
            print(tab)
        
        if correct:
            if numAuto:
                dico['class'] = position
            dico['temps'] = dico['temps'].strip()
            dico['cat'] = dico['cat'].strip()
            if 'club' not in dico.keys():
                dico['club'] = ''
            if 'sexe' not in dico.keys():
                dico['sexe'] = ''
            if len(dico['temps']) == 5:
                dico['temps'] = '0:{}'.format(dico['temps'])
            if 'prenom' in dico.keys():
                dico['nom'] = dico['nom'] + ' ' + dico['prenom']
            coureur = checkFormat(dico)
            coureurs.append(coureur)
    if suite:
        return coureurs
    else:
        exit(66)

def checkFormat(coureur):
    #
    # print(coureur)
    # si le temps est affiché avec des quotes alors on le transforme avec des :
    if '\'\'' in coureur['temps']:
        coureur['temps'] = coureur['temps'].replace('\'\'', '')
        coureur['temps'] = coureur['temps'].replace('\'', ':')
        coureur['temps'] = coureur['temps'].replace('h', ':')
        print(coureur['temps'])

    if (coureur['sexe'] == '' and (coureur['cat'][-1] == 'H' or coureur['cat'][-1] == 'M')) or coureur['sexe'] == 'H':
        coureur['sexe'] = 'M'
    elif coureur['sexe'] == '' and (coureur['cat'][-1] == 'F' or coureur['cat'][-1] == 'F'):
        coureur['sexe'] = 'F'
    #
    if 'VET ' in coureur['cat']:
        coureur['cat'] = coureur['cat'].replace('VET ', 'V')
    if coureur['cat'] == 'C':
        coureur['cat'] = 'CA'
    if coureur['cat'] == 'JUN':
        coureur['cat'] = 'JU'
    # coureur['cat'] = coureur['cat'].split('/')[1][0:2]
    if coureur['club'] == '-' or coureur['club'] == '0' or coureur['club'] == 'NL' or coureur['club'] == '*':
        coureur['club'] = ''
    if 'Non Licencie' in coureur['club']:
        coureur['club'] = ''
    return coureur

def lstCSV(coureurs):
    coureursCSV = []
    for coureur in coureurs:
        ligne = u'{};{};{};{};{};{};\n'.format(coureur['class'], coureur['temps'], coureur['nom'], coureur['cat'][0:2], coureur['sexe'], coureur['club'].strip())
        coureursCSV.append(ligne)
    return coureursCSV

def writeCsv(coureurs, FICCSV):
    with open(FICCSV, 'w')as out:
        out.write('class;temps;nom;cat;sexe;club\n')
        for coureur in coureurs:
            # print(coureur)
            #ligne = u'{};{};{};{};{};{};\n'.format(coureur['class'], coureur['temps'], coureur['nom'], coureur['cat'][0:2], coureur['sexe'], coureur['club'].strip())
            out.write(coureur)

def checkCoureurs(coureurs):
    '''verification du fichier produit et creation d'un tableau des anomalies'''
    cat = ['SE', 'V1', 'V2', 'V3', 'V4', 'V5', 'JU',
           'CA', 'ES', 'MI', 'BE', 'PO', 'EA', 'HD', 'HA']
    sex = ['M', 'F']
    anos = {}
    i = 0
    for coureur in coureurs:
        ligneCSV = u'{};{};{};{};{};{};\n'.format(coureur['class'], coureur['temps'], coureur['nom'], coureur['cat'][0:2], coureur['sexe'], coureur['club'].strip())
        i += 1
        ligne = ligneCSV.split(';')
        #print('-----------', ligne)
        # verification sequencement dans le classement
        try:
            if int(ligne[0]) != i:
                # print 'anomalie dans la sequence du classement'
                # print("i : ", i, "--- classement : ", int(ligne[0]))
                if 'sequencement' not in anos.keys():
                    anos['sequencement'] = []
                anos['sequencement'].append(
                    'classement attendu {}, trouve {} : {}'.format(i, int(ligneCSV[0]), ligne))
        except:
            pass
            #print('sequencement : ', ligne)
        #
        # verification caractere pourri <.>
        if [pourri for pourri in ligne if '.' in pourri]:
            if 'point' not in anos.keys():
                anos['point'] = []
            anos['point'].append(
                'caractere <.> interdit dans {}'.format(ligne))
        #
        # verification caractere pourri <?>
        if [pourri for pourri in ligne if '?' in pourri]:
            if 'interro' not in anos.keys():
                anos['interro'] = []
            anos['interro'].append(
                'caractere <?> interdit dans {}'.format(ligne))
        #
        # verification du temps
        try:
            datetime.strptime(ligne[1], '%H:%M:%S')
        except:
            # print 'Probleme de format <temps> : {}'.format(lignes)
            if 'temps' not in anos.keys():
                anos['temps'] = []
            anos['temps'].append(
                'format non correct : [{}] dans {}'.format(ligne[1], ligne))
        #
        # verification nom/prenom
        if '.' in ligne[2]:
            if 'nom/prenom' not in anos.keys():
                anos['nom/prenom'] = []
            anos[
                'nom/prenom'].append('caractere <.> interdit dans le nom/prenom : {}'.format(ligne))
        #
        # verification de la categorie
        if len(ligne[3]) != 2:
            if 'categorie' not in anos.keys():
                anos['categorie'] = []
            anos['categorie'].append(
                'longeur non correcte : [{}] dans {}'.format(ligne[3], ligne))
        if ligne[3] not in cat:
            if 'categorie' not in anos.keys():
                anos['categorie'] = []
            anos['categorie'].append(
                'format non reconnu : [{}] dans {}'.format(ligne[3], ligne))
        #
        # verification sexe (...)
        if ligne[4] not in sex:
            if 'sexe' not in anos.keys():
                anos['sexe'] = []
            anos['sexe'].append(
                'attendu <M> ou <F> , trouve {} : dans {}'.format(ligne[4], ligne))
        #
    return anos

def main(argv):
    '''Traitement d'un fichier csv : 
       - premier param : nom du fichier à traiter
       - deuxieme param(facultatif) : genere sequentiellement le classement en cas de doublon'''
    fic = argv[0]
    if len(argv) == 2:
        numAuto = True
    else:
        numAuto = False
    fic_sans_extension = os.path.splitext(os.path.basename(fic))[0]
    fic_avec_extension = os.path.basename(fic)
    FIC     = '{}{}{}'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/source/', fic_avec_extension)
    FICCSV  = '{}{}{}.csv'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/source/', fic_sans_extension)
    FICDEST = '{}{}{}.csv'.format(os.environ['HOME'], '/nextcloud/kikourou/fichiers/csv/'   , fic_sans_extension)
    coureurs = lecFic(FIC, numAuto)
    coureursCSV = lstCSV(coureurs)
    anomalies = checkCoureurs(coureurs)
    if len(anomalies.items()) == 0:
        writeCsv(coureursCSV, FICCSV)
        print(BOLD, "Fichier {} correct".format(FICDEST), RESET)
        # on bascule le csv dans fichier/csv
        fic = "cp {} {}"
        cp = os.system(fic.format(FICCSV, FICDEST))
        # on sauve le source
        fic = "mv /home/paulo/nextcloud/kikourou/fichiers/source/{}*  /home/paulo/nextcloud/kikourou/fichiers/source/sv_fic_source"
        sv = os.system(fic.format(fic_sans_extension))
    else:
        print(BOLD, "Fichier {} pourri".format(FICCSV), RESET)
        for cle, valeur in anomalies.items():
            print(BOLD, "\nAnomalie de type : ", cle, RESET)
            for ano in valeur:
                print('\t{}'.format(ano))
    return 0

if __name__ == '__main__':
    main(argv[1:])
