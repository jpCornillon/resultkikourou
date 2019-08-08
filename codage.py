#!/usr/bin/python3
# -*- coding: utf8

import sys
import codecs
import encodings
import chardet

# fic = '/home/paulo/nextcloud/kikourou/fichiers/source/sassenage11.csv'

# code = 'utf8'

# le code 'windows-1250' fonctionne pour la ligne ci-dessous
# zob = u'4;00:38:22;PELLM-I Ludovic;V1;M;CMI^M$'


def detect_code(fic):
    '''retourne l'encodage du fichier'''
    rawdata = open(fic, 'rb').read()
    return chardet.detect(rawdata)['encoding']

def main(argv):
    print(detect_code(argv))
    with open(argv, 'r', encoding=detect_code(argv)) as f:
    	alls = f.readlines()
    with open('{}-OK'.format(argv), 'w') as f:
    	for a in alls:
    		f.write('{}\n'.format(a.strip()))

#
#####################################################
#
if __name__ == '__main__':
    main(sys.argv[1])
#
#####################################################



#with open(fic, 'rb' ) as f:
#	alls = f.readlines()
#print(alls)
#for a in alls:
#	for code in sorted(set(encodings.aliases.aliases)):
#		print(a)
#		print('code : ', code, ' --> ',a.translate(code))
	# print("**** ",code.decode())
	# try:
	# 	print('code : ', code)
	# 	print(codecs.decode(zob, code))
	# except:
	# 	pass
	# 	#print('Imbittable !!!')


	# with codecs.open(fic, 'r', encoding=code) as f:
	# 	try:
	# 		f.read()
	# 		print('code {} correct pour le fichier {}'.format(code, fic))
	# 		exit(1)
	# 	except:
	# 		print()
	# 		# print('code {} non utilisable pour ce fichier'.format(code))

