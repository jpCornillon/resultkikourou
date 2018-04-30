#!/bin/bash
#
# <JPC>
# caracter BOM (premiere ligne d'un fichier)
# suppression de "M-oM-;M-?Place;Temps;Nom;Cat;Sexe;Club" sur la premiere ligne
#   d'un fichier
# sed -i -e '1s/^.//' chassieu.csv
#          OU         
# dans vim : 
# sauvegarde sans le BOM : :setlocal nobomb 
# demande a vim si BOM : :setlocal bomb?
# repond bomb si BOM present ou nobomb si BOM non present
#          OU         
# dos2unix fait la suppression du BOM en début de premiere ligne et les ctrl^m de fin 
#
#
#
# </JPC>
#

#############################################################################
# SCRIPT:   M-BM-Remover.sh
# DESCRIPTION:
#           This script will be able to detect hidden caracter "M-BM-",
#               And/Or remove this !
# REVISIONS:
#           2014/06/11  YG
#____________________________________________________________________________
#
# PARAMETERS:
#  > $1  :TARGET,      (e.g. '"*.sh"' )
#  > $2  :ACTION,      (e.g. 'remove' )
#  > $2  :BACKUP,      (e.g. '' )
#
#############################################################################

TARGET=$1
ACTION=$2
BACKUP=$3

if [ "$TARGET" = "" ]
then
    echo 'Need to choose target file'
    echo 'M-BM-Remover [TARGET] [show/remove] [backup]'
    echo 'Example : M-BM-Remover "*.sh" remove backup'
    exit
fi

echo "ACTION = $ACTION";
echo "TARGET = $TARGET";
echo

if [ "$ACTION" = "show" ]
then
    for file in $TARGET
    do
        if [ "$file" != "M-BM-Remover.sh" ]
        then
            echo "Traitement de $file ..."
            cat -v $file | grep M-BM-
            NB=`cat -v $file | grep M-BM- | wc -l`
            echo "Occurence(s) : $NB"
        fi
    done 
fi

if [ "$ACTION" = "remove" ] || [ "$ACTION" = "" ]
then
    for file in $TARGET
    do
        if [ "$file" != "M-BM-Remover.sh" ]
        then
            echo "Traitement de $file ..."
            NB=`cat -v $file | grep M-BM- | wc -l`
            if [ "$BACKUP" = "backup" ]
            then
                cat $file > $file.bak
            fi
            cat -v $file.bak | sed s/M-BM-//g > $file
            echo "Occurence(s) removed : $NB"
        fi
        echo
    done 
fi

