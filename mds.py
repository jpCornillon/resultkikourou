#!/usr/bin/python3
# -*- coding: utf8
#
import os
import sqlite3
import requests
from urllib.request import urlopen, ProxyHandler
from bs4 import BeautifulSoup
import re
from time import sleep

# fic = '/home/paulo/dropbox/kikourou_ori/fichiers/source/mdsPaulo.csv'
fic = '/home/paulo/dropbox/kikourou_ori/fichiers/source/mdsKikou.htm'
html = open(fic, 'rb')
soup = BeautifulSoup(html, 'lxml')
for tr in soup.select("tr"):
    zob = [ '{};'.format(i.text) for i in tr.findAll('td') if ',' not in tr.text ]
    print(''.join(zob))
#    for td in tr.select("td"):
#        print(td)
