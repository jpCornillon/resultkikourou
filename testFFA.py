#!/usr/bin/python3
# -*- coding: utf8


from urllib.request import urlopen, ProxyHandler
from bs4 import BeautifulSoup
url = 'http://bases.athle.com/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison=2017&frmtype1=Hors+Stade&frmtype2=&frmtype3=&frmtype4=&frmniveau=&frmniveaulab=&frmligue=&frmdepartement=&frmeprrch=&frmclub=&frmdate_j1=1&frmdate_m1=7&frmdate_a1=2017&frmdate_j2=30&frmdate_m2=7&frmdate_a2=2017'
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
table = soup.find('table', id='ctnResultats')
for tr in soup.findAll('tr'):
    td = [td for td in tr.findAll('td')]
    import pdb; pdb.set_trace()
