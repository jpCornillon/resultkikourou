Outils de saisie de résultats sur KiKourou
======
[![License](https://img.shields.io/pypi/l/osmapi.svg)](https://github.com/jpCornillon/tstResultKikou/blob/master/LICENCE)

Scripts python facilitant la saisie de résultats sur KiKourou :
- extraction pdf
- mise en forme csv/txt
- consultation/telechargement resutat FFA
- inversion nom_prenom 

## Prérequis

### [python3]
* [python-requests](https://pypi.org/project/requests/) - HTTP library, written in Python, for human beings
```bash
sudo yum install python3-requests [ou] pip install requests
```
* [python3-urllib3](http://urllib3.readthedocs.org/) - HTTP module with connection pooling and file POST abilities
```bash
sudo yum install python3-urllib3 [ou] pip install urllib3
```
* [python3-beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/) - HTML/XML parser
```bash
sudo yum install python3-beautifulsoup4 [ou] pip install beautifulsoup4 
```

### Utilisation du script 'kikourou.py'
Produit : 
- dans le meilleur des cas un fichier csv correct dans $HOME/nextcloud/kikourou/fichier/csv/
- une liste d'anomalies à corriger (dans un fichier 'nom_de_la_course'.txt
- rien du tout !

Plusieurs options d'utilisation du script
- traitement d'un fichier :
```bash
./kikourou.py $HOME/nextcloud/kikourou/fichiers/source/course.[pdf, csv]
```

- consultation résultat base FFA [annee: 2016, mois: Juillet, departement: 73]
```bash
./kikourou.py calendrier -a 2016 -m 7 -d 073
```

- résultat d'une compét en fonction du num renvoyé par la commande précedente [ -n numero course -f fichier_en_sortie ] :
```bash
./kikourou.py course -n 187293 -f villarroger
```


### Utilisation du script 'inv_nom_prenom.py'
Utilisation :
Le script (à modifier avec le nom de la course) permet d'inverser nom/prenom d'un fichier csv
Produit : 
- un fichier (nom à definir dans le script) avec les nom-prenom inversé
- une liste de coureur avec des noms composés
- une liste de coureur pour lesquels le script n'a rien compris !


### Utilisation du script 'all_result.py'
Utilisation : 
- avant de lancer ce script, il faut creer un fichier htm [ $HOME/nextcloud/kikourou_files/resultat.htm ] qui contient la liste des résultats de course que l'on veut récupérer (depuis www.kikourou.net)
Il faut faire un copier-coller de la balise '<ul>....</ul>' dans le fichier htm (ça prend un peu de temps, il y a beaucoup de  résultat et c'est du html...)
![Preview](kikourou.png 'copier la balise <ul>...</ul>')
- faire un peu de ménage dans le fichier obtenu : supprimer tous les premiers résultats par exemple permet de gagner pas mal de temps
et d'eviter des acces sur la base de la FFA (si ils sont toujours là, c'est que le passage précedent ne les a pas trouvé...)
Lancement :
```bash
./all_resultat.py
```
Le script extrait les url du fichier, recupère la date, lieu, departement de la course puis se connecte sur la base FFA afin de voir si le résultat existe. Si oui, le prog produit (ou pas) un fichier csv correct.
En résumé, le script parcourt les resultats kikourou et tente de trouver un résultat dans la base FFA...


### Utilisation du script 'genCSV.py'
Utilisation : 
Ce script est utilisé dans 'kikourou.py' mais peut aussi se lancer en ligne de commande. Il suffit de lui passer un fichier en entre (.csv ou .txt).
Après diverses gruikeries, il produit (ou pas) un fichier csv correct.
Lancement :
```bash
./gesCSV.py $HOME/nextcloud/kikourou/files/course.csv
```

### Utilisation du script 'conv.sh'
Utilisation : 
Ce script tente de résoudre les problèmes d'encodage sur les fichiers transmis :
- sauvegarde du fichier
- decodage du code
- encodage en utf8
Il peut être utilisé directement dans le terminal mais il est aussi utilisé dans 'kikourou.py'
Lancement :
```bash
./conv.sh $HOME/nextcloud/kikourou/files/course.csv
```
