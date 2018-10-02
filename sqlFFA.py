#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#modules
import sys
import sqlite3
#
class BaseFFA(object):
    """docstring for baseFFA"""

    def __init__(self):
        super(BaseFFA, self).__init__()
        self.db = sqlite3.connect('sql/baseFFA.db')
        
    def readDB(self, *kargs, **kwargs):
        dic = dict({'aa': 'annee', 'mm': 'mois', 'jj':'jour', 'd': 'departement', 'v': 'ville'})
        #sqlbase = 'select annee, mois, jour, ville, titre, numero, departement from resultats'
        if len(kwargs.keys()) == 0:
            sql = 'select annee, mois, jour, ville, titre, numero, departement from resultats'
        elif len(kwargs.keys()) == 1:
                sqlbase = 'select annee, mois, jour, ville, titre, numero, departement from resultats'
                where = ' where {}={}'
                k = ','.join(kwargs.keys())
                # <moche>
                if k == 'v': kwargs[k]="'{}'".format(kwargs[k])
                if k == 'd': kwargs[k]="'{}'".format(kwargs[k])
                # </moche>
                sql = sqlbase + where.format( dic[k], kwargs[k] )
        else:            
            add_where = ''
            sqlbase = 'select annee, mois, jour, ville, titre, numero, departement from resultats where '
            i = 0
            for k, v in kwargs.items():
                # <moche>
                if k == 'v': kwargs[k]="'{}'".format(kwargs[k])
                if k == 'd': kwargs[k]="'{}'".format(kwargs[k])
                # </moche>
                if i == 0:
                    i = 1
                    where = ' {}={} '
                    add_where += where.format(dic[k], kwargs[k])
                else:
                    where = ' and {}={}'
                    add_where += where.format(dic[k], kwargs[k])
                sql = sqlbase + add_where
            # print('sql : ', sql)
            #VOIR CASE SUR LES REQUETES WHERE 
            #VOIR UN EVENTUEL LIKE

        db = sqlite3.connect('sql/baseFFA.db')
        cursor =db.cursor()
        cursor.execute(sql)
        for row  in cursor:
            print('{:04}-{:02}-{:02}  {:25}: {} N°{:6} ({:3})'.format(*row))
            
    def ficCSV(self, fic):
        with open(fic, 'r') as f:
            for line in f.readlines():
                annee, mois, jour, departement, ville, numero, titre = line.strip().split(';')
                d = (annee, mois, jour, departement, ville, numero, titre)  
                self.insertDB(d)
        return

def main(argv):
    if len(argv) == 0:
        param={}
    else:
        param = { k : v for k, v in [ i.split('=') for i in argv ]}

    ffa = BaseFFA()
    ffa.readDB(**param)
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])

