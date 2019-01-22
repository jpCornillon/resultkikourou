#!/bin/bash

login='pauloTrail'
pass='43paulotrail69'
sid='86f9ffaaa9e34d56ff5cd95fb5d8062e'
url1='http://www.kikourou.net/forum/ucp.php'
url2='http://www.kikourou.net/resultats/ajoutresultat.php'

#Récupération des premiers cookies
wget -dO /dev/null --cookies=on --keep-session-cookies --save-cookies=cookies.txt $url1

#Deuxième passage pour récupérer les cookies sécurisés
wget -dO /dev/null --cookies=on --keep-session-cookies --save-cookies=cookies.txt          \
                   --load-cookies=cookies.txt                                              \
                   --post-data "mode=login&username=$login&password=$pass&sid=$sid" \
                   $url1

#Troisième passage pour se connecter
wget -dO $url2  --cookies=on --keep-session-cookies --save-cookies=cookies.txt --load-cookies=cookies.txt --post-data  "mode=login&username=$login&password=$pass&sid=$sid" 
