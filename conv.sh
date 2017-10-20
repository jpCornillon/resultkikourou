#!/bin/bash
if [ $# -lt 1 ] 
then
    echo '-------------------------------------------------------------'
    echo '-- Un parametre attendu (nom de fichier a convertir) !!!!! --'
    echo '-------------------------------------------------------------'
    exit 1
fi
#dir='/home/xxxxx/dropbox/kikourou/fichiers/source/'
dir=''
nomfic=${1}
svfic=${1}_av_iconv
cod_in=$(file ${nomfic}|cut -d' ' -f2)
cod_ext='utf8'
#cod_ext='ISO-8859-1'
#cod_ext='ascii//TRANSLIT'
#
if [ ${cod_in} = 'ISO-8859' ]
    then 
        code='ISO8859-1'
        #echo '   ---> fichier déja codé en Iso-8859, on ne fait rien !'
        #exit 1
elif [ ${cod_in} = 'UTF-8' ]
    then
        #echo '   ---> fichier déja codé en Utf8, on ne fait rien !'
        #exit 1 
        code='UTF8'
elif [ ${cod_in} = 'HTML' ]
    then 
        code='UTF8'
# tentative pour fichier tout pourri
elif [ ${cod_in} = 'Non-ISO' ]
    then
        code='863'
elif [ ${cod_in} = 'ASCII' ]
    then
        echo '   ---> fichier déja codé en Ascii, on ne fait rien !'
        exit 1
else
    echo '   ---> format de fichier non reconnu   !!!! '
    exit 66
fi
# sauvegarde du fichier d'origine
echo "- copie du fichier $(basename ${nomfic}) en  $(basename ${svfic})"
cp  ${dir}${nomfic} ${dir}${svfic}
#
#cat ${dir}${nomfic}|iconv -f ${code} -t ${cod_ext} > ${dir}prov
cat ${dir}${nomfic}|iconv -f ${code} -t utf8 > ${dir}prov
mv ${dir}prov  ${dir}${nomfic}
echo "- fichier  $(basename ${nomfic}) recodé de ${cod_in} en ${cod_ext}"
