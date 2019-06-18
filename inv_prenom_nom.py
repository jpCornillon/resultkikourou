#!/usr/bin/python3
# -*- coding: utf8
#
#####################################################
#
import os
import sys
import re
#
#####################################################
#globales
#import pdb; pdb.set_trace()
BOLD = "\033[1m"
RESET = "\033[0;0m"
CSV='class;temps;nom;club;f1;cat\n'
#
def main():
    '''A modifier : 
            - nom du fichier en entree
            - nom du fichier en sortie
            - indice de la zone de nom
    '''
    ficin = '/home/paulo/dropbox/kikourou_ori/fichiers/source/allo66.csv'
    ficout = '/home/paulo/dropbox/kikourou_ori/fichiers/source/allo66_inverse.csv'
    anos=[]
    with open(ficin) as fic:
       coureurs = [ i.split(';') for i in fic.readlines() ]
    for i in coureurs:
        #print(i)
        j = i[2].split()
        if len(j) == 2:
            j.reverse()
            i[2]=' '.join(j)
        elif len(j) == 3:
            print('Prenom composé --> {}'.format(j))
            p1, p2, n = j
            if p2 == p2.upper():
                j = '{} {} {}'.format(p2, n, p1)
            else:    
                j = '{} {} {}'.format(n, p1, p2)
            i[2] = j
        elif len(j) > 3:
            print(BOLD + 'Attention : c\'est le bordel  --> {}'.format(j) + RESET)
            print(BOLD + 'JE NE FAIS RIEN' + RESET)
            anos.append(j)
            i[2] = ' '.join(j)
            print(i[2])
        #i[2]=' '.join(j)
    #for i in coureurs: print(i)
    if len(anos) > 0 :
        for ano in anos: print(ano)
        #exit(666)
    fic = open(ficout,'w')
    for coureur in coureurs:
        #ligne= '{}\n'.format(';' .join(coureur).encode('ascii','ignore'))
        ligne= '{}\n'.format(';' .join(coureur))
        fic.write(ligne)
    fic.close()
#
#####################################################
#
if __name__ == '__main__':
    main()
#
#####################################################
