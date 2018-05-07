patterns = \
   (  
         (r'[\n\r\t]', '', False )                                         ,  # tous les caracteres pourris de tabulation (tab, rc, ...)
         (r'[?"]', '', False)                                              ,  # tous les caracteres a supprimer
         (r'M-oM-;M-?', '', True)                                          ,  # fichier pourri suppression du BOM en premiere ligne
         (r'M-CM-\)', 'e', True)                                           ,  # fichier pourri convertit 'M-CM-' en e
         (r'M-CM-^I', 'E', True)                                           ,  # fichier pourri convertit 'M-CM-^I' en E
         (r'M-CM-^@', 'A', True)                                           ,  # fichier pourri convertit 'M-CM-^@' en A
         (r'M-BM-', '', True)                                              ,  # fichier pourri convertit 'M-BM-' en rien
         (r'[éèêë]', 'e', False)                                           ,  # remplacement des accents
         (r'[ÉÈÉÈÊË]', 'E', False)                                         ,  # remplacement des accents
         (r'[C]', 'C', False)                                              ,  #remplacement des accents
         (r'[Ç]', 'C', False)                                              ,  #remplacement des accents
         (r'[ÔÓ]', 'O', False)                                             ,  #remplacement des accents
         (r'[ÎÏÌÍ]',   'I', False)                                         ,  #remplacement des accents
         (r'[àâ]',  'a', False)                                            ,  #remplacement des accents
         (r'[ÀÂÄÃÁ]',  'A', False)                                         ,  #remplacement des accents
         (r'[îï]',   'i', False)                                           ,  #remplacement des accents
         (r'[ç]',   'c', False)                                            ,  #remplacement des accents
         (r'[ô]',   'o', False)                                            ,  #remplacement des accents
         (r'[ù]',   'u', False)                                            ,  #remplacement des accents
         (r'[°]',   '' , False)                                            ,  #remplacement des accents
         #(r'\(\)',  '' , True)                                             ,  #remplacement de '()' le 03 mai 2017
         (r'\.com',   '-com' , True)                                       ,  #remplacement de '.com'
         (r'\.fr',   '-fr' , True)                                         ,  #remplacement de '.fr'
         (r'\.cat',   '-cat' , True)                                       ,  #remplacement de '.cat'
         (r'\.dk',   '-dk' , True)                                         ,  #remplacement de '.dk'
         (r'\.lv',   '-lv' , True)                                         ,  #remplacement de '.lv'
         (r'^([0-9]+)[\.];', r'\1;', False)                                ,  #sup . dans le classement type '62.;'
         (r';[a-zA-Z][0-9]{4,8}[a-zA-Z]?[;$]', ';', False)                 ,  #sup chaines pourries
         (r';[0-9]{6,20};', ';', False)                                    ,  #sup chaines pourries type ';012526522'
         (r';[0-9]{3,20}[_-][0-9]{3,20};', ';', False)                     ,  #sup chaines pourries type ';0125_26522'
         (r';[0-9]{3,20}[_-][0-9]{3,20};', ';', False)                     ,  #sup chaines pourries type ';0125_26522'
         # (r';;', ';', False)                                             ,  #sup chaines pourries type ';;'
         (r'\/[0-9]+;',   ';' , True)                                      ,  #remplacement de '/1;' 
         #(r';[0-9]+;', ';', False)                                        ,  #sup chaine type ';2564;'
         #(r';[0-9]+$', ';', False)                                         ,  #pareil ci-dessus mais en fin de ligne ';2564'
         #(r';[A-Z][A-Z-][A-Z];', ';', True)                               ,  #suppression zone de type 'AUV' ou 'R-A' (pas bon car supprime aussi SEM ...)
         ##################################################################
         #DATE DE NAISSANCE
         ##################################################################
         (r';[0-9][0-9][/][0-9][0-9][/][0-9][0-9]$', '', False)            ,  #sup date de naissance type ';08/09/16$'
         (r';[0-9][0-9][/][0-9][0-9][/][0-9][0-9]?[; ]', ';', False)       ,  #sup date de naissance type '08/09/16'
         (';\[.*\] ', ';', False)                                          ,  #sup des crochets et de leur contenu '[kegmg564]'
         #(r';FRA;', ';', False)                                            ,  #sup chaine type ';FRA;'
         #(r';FRA $', '' , False)                                           ,  #sup chaine type ';FRA'
         #(r';FRA [nN][0-9]+[ ]?;', ';', False)                             ,  #sup chaine type ';FRA n522;' avec un espace optionnel avant le point virgule
         #(r';FRA [0-9]+[ ]?;', ';', False)                                 ,  #sup chaine type ';FRA 1874522;' avec un espace optionnel avant le point virgule
         #(r';FRA [A-Z][ ]?;', ';', False)                                  ,  #sup chaine type ';FRA E;' avec un espace optionnel avant le point virgule
         #(r';BEL$', '' , False)                                            ,  #sup chaine type ';BEL'
         #(r';ITA$', '' , False)                                            ,  #sup chaine type ';ITA'
         #(r';GER$', '' , False)                                            ,  #sup chaine type ';GER'
         #(r';SUI$', '' , False)                                            ,  #sup chaine type ';SUI'
         #(r';NED$', '' , False)                                            ,  #sup chaine type ';NED'
         #(r';POR$', '' , False)                                            ,  #sup chaine type ';POR'
         #(r';BEL $', '' , False)                                           ,  #sup chaine type ';BEL'
         #(r';ITA $', '' , False)                                           ,  #sup chaine type ';ITA'
         #(r';GER $', '' , False)                                           ,  #sup chaine type ';GER'
         #(r';SUI $', '' , False)                                           ,  #sup chaine type ';SUI'
         #(r';NED $', '' , False)                                           ,  #sup chaine type ';NED'
         #(r';POR $', '' , False)                                           ,  #sup chaine type ';POR'
         (r';n[0-9]+;', ';', False)                                        ,  #sup chaine type ';n12569;'
         ##################################################################
         # CLUB
         ##################################################################
         (r'42.195', '42-195', False)                                      ,  #sup point dans le club '42.195'
         (r';NL;', r';', True)                                             ,  #modif cat 'NL' (non licencié)
         (r';non licenci[eé];', r';', True)                                ,  #modif cat 'NL' (non licencié)
         (r';non licenci[eé]$', r'', True)                                 ,  #modif cat 'NL' (non licencié)
         ##################################################################
         # CATEGORIE
         ##################################################################
         (r';([MF])SE',  r';SE\1', True)                                   ,  #modif cat type ';MSE'
         (r';([MF])VE',  r';V1\1', True)                                   ,  #modif cat type ';MSE'
         (r';[0-9]+ ', ';', False)                                         ,  #sup numero devant la cat
         (r';([A-Z][A-Z12345]) ([FH])',  r';\1\2', False)                  ,  #sup /numero apres la cat
         (r';([0-9]+[A-Z] )(.*)', r';\2', True)                            ,  #modif cat (ignorecase)
         (r';([A-Z][A-Z][A-Z])(/[0-9]+)', r';\1', True)                    ,  #modif cat (ignorecase) type ';SEM/85'
         (r';(VETERAN) ([0-9]) ([HMF])', r';V\2\3', True)                  ,  #modif cat (ignorecase)
         (r';(VETERAN) ([0-9])', r';V\2', True)                            ,  #modif cat (ignorecase)
         (r';SENIOR', r';SE', True)                                        ,  #modif cat (ignorecase)
         (r';(SENIOR) ([HMF])' , r';SE\2', True)                           ,  #modif cat (ignorecase)
         (r';(ESPOIR) ([HMF])' , r';ES\2', True)                           ,  #modif cat (ignorecase)
         (r';ESPOIR' , r';ES', True)                                       ,  #modif cat (ignorecase)
         (r';(MINIME) ([HMF])' , r';MI\2', True)                           ,  #modif cat (ignorecase)
         (r';(JUNIOR) ([HMF])' , r';JU\2', True)                           ,  #modif cat (ignorecase)
         (r';JE;' , r';JU;', True)                                         ,  #modif cat (ignorecase)
         (r';JEM;' , r';JUM;', True)                                       ,  #modif cat (ignorecase)
         (r';JEM$' , r';JUM', True)                                        ,  #modif cat (ignorecase)
         (r';(CADET) ([HMF])'  , r';CA\2', True)                           ,  #modif cat (ignorecase)
         (r';(POUSSIN) ([HMF])', r';PO\2', True)                           ,  #modif cat (ignorecase)
         (r';(master)[ ]?([0-9])[ ]?([HMF])', r';V\2\3', True)             ,  #modif cat (ignorecase) avec ou sans espace entre les zones type 'Master 1 H'
         (r';(MASTER)[ ]', r';V', True)                                    ,  #modif cat (ignorecase) type 'Master 1'
         (r'master ([0-5])', r'V\1', True)                                 ,  #modif cat (ignorecase) type 'Master 1'
         (r';MAS([0-9]);', r';V\1;', True)                                 ,  #modif cat (ignorecase) type 'Master 1'
         (r';(M)([0-9])([HMF])', r';V\2\3', True)                          ,  #modif cat (ignorecase) type 'M1H'
         (r';M([0-5])', r';V\1', True)                                     ,  #modif cat (ignorecase) type 'M1'
         (r';VM([123])', r';V\1', True)                                    ,  #modif cat (ignorecase) type ';VM1'
         (r';VE;', r';V1;', True)                                          ,  #modif cat (ignorecase) type ';VE'
         (r';VE$', r';V1', True)                                           ,  #modif cat (ignorecase) type ';VE'
         (r';VE([MF]);', r';V1\1;', True)                                  ,  #modif cat (ignorecase) type ';VEM'
         (r';VE([MF])$', r';V1\1', True)                                   ,  #modif cat (ignorecase) type ';VEM'
         (r';VE([F]);', r';V1\1;', True)                                   ,  #modif cat (ignorecase) type ';VEM'
         (r';VE([F])$', r';V1\1', True)                                    ,  #modif cat (ignorecase) type ';VEM'
         (r'[.]([HF];)', r'\1', False)                                     ,  #sup du point dans la cat
         (r';(S)([HMF])', r';SE\2', True)                                  ,  #modif cat (ignorecase) type 'SH'
         (r';(VH)([0-9])', r';V\2M', True)                                 ,  #modif cat (ignorecase) type 'VH1'
         (r';(V)([MF])([0-9])', r';\1\3\2', True)                          ,  #modif cat (ignorecase) type 'VH1'
         (r';(POUSSIN) ([HMF])', r';PO\2', True)                           ,  #modif cat (ignorecase)
         (r';SE-H',  r';SEM', True)                                        ,  #modif cat type 'SE-H'
         (r';SE-D',  r';SEF', True)                                        ,  #modif cat type 'SE-D'
         (r';Se;',   r';SE;', False)                                       ,  #modif cat type ';Se;'
         (r';Ca;',   r';CA;', False)                                       ,  #modif cat type ';Ca;'
         (r';Ju;',   r';JU;', False)                                       ,  #modif cat type ';Je;'
         (r';Es;',   r';ES;', False)                                       ,  #modif cat type ';Es;'
         (r';(V[1-5])(-H);',  r';\1M;', True)                              ,  #modif cat type 'V1-H'
         (r';(V[1-5])(-D);',  r';\1F;', True)                              ,  #modif cat type 'V1-D'
         (r';(V)([fhm])([0-9]);',  r';V\3\2;', True)                       ,  #modif cat type 'VF1'
         (r';S([FHM]);',  r';SE\1;', True)                                 ,  #modif cat type 'SF'
         (r';J([FHM]);',  r';JU\1;', True)                                 ,  #modif cat type 'JF'
         (r';Homme', r';M', True)                                          ,  #modif cat type 'Homme'
#         (r' HOMME', r'M', False)                                          ,  #modif cat type ' HOMME'
         (r';HOMME', r'M', False)                                          ,  #modif cat type ';HOMME'
#         (r'HOMME' , r'M', False)                                         ,  #modif cat type 'HOMME'
#         (r' FEMME', r'F', False)                                          ,  #modif cat type ' FEMME'
         (r'FEMME' , r'F', False)                                          ,  #modif cat type 'FEMME'
         (r'Homme\/V([1234])', r';V\1M', True)                             ,  #modif cat type 'Homme/V1'
         (r'Femme\/V([1234])', r';V\1F', True)                             ,  #modif cat type 'Femme/V1'
         (r'Homme\/Senior', r';SEM', True)                                 ,  #modif cat type 'Homme/Senior'
         (r'Femme\/Senior', r';SEF', True)                                 ,  #modif cat type 'Femme/Senior'
         (r'Homme\/Cadet', r';CAM', True)                                  ,  #modif cat type 'Homme/Cadet'
         (r'Femme\/Cadet', r';CAF', True)                                  ,  #modif cat type 'Femme/Cadet'
         (r'([MFH])\/Senior', r';SE\1', True)                              ,  #modif cat type 'M ou F /Senior'
         (r'([MFH])\/Junior', r';JU\1', True)                              ,  #modif cat type 'M ou F/Junior'
         (r'([MFH])\/Cadet', r';CA\1', True)                               ,  #modif cat type 'M ou F/Cadet'
         (r'([MFH])\/Espoir', r';ES\1', True)                              ,  #modif cat type 'M ou F/Espoir'
         (r'([MFH])\/V([1234])', r';V\2\1', True)                          ,  #modif cat type 'M/V1'
         (r';HSe', r';SEM', False)                                         ,  #modif cat type ';HSe'
         (r';HEs', r';ESM', False)                                         ,  #modif cat type ';HEs'
         (r';HV([0-9])', r';V\1M', False)                                  ,  #modif cat type ';HV1'
         (r';Dame',  r';F', True)                                          ,  #modif cat type 'Dame'
         (r';Cadet',  r';CA', True)                                        ,  #modif cat type 'Cadet'
         (r';Junior',  r';JU', True)                                       ,  #modif cat type 'Junior'
         (r';([MHF])\.',  r';\1', True)                                    ,  #modif cat type ';M1'
         (r';([0-9])([MFH]);', r';\2;', True)                              ,  #mod classement '1 M'
         (r';([MF])SE',  r';SE\1', True)                                   ,  #modif cat type ';MSE'
         (r';([MF])VE',  r';V1\1', True)                                    ,  #modif cat type ';MVE'
         (r';([MF])V([0-9])',  r';V\2\1', True)                            ,  #modif cat type ';MV1'
         (r';([MF])ES',  r';ES\1', True)                                   ,  #modif cat type ';MV1'
         (r';([MF])MI',  r';MI\1', True)                                   ,  #modif cat type ';MMI'
         (r';([MF])JU',  r';JU\1', True)                                   ,  #modif cat type ';MJU'
         (r';([MF])CA',  r';CA\1', True)                                   ,  #modif cat type ';MCA'
         (r' ?\(.{1,4}\);', ';', False)                                    ,  #modif cat : sup de paranthese avec blanc avant ou apres type "(9 / 58);"
         (r' ?\(.{1,3}\) ?', '', False)                                    ,  #modif cat : sup de paranthese avec blanc avant ou apres type "(9 / 58);" 
         (r';\+[0-9]+:[0-9]+:[0-9]+', ';', False)                          ,  #sup chaine du type '+xxxx' 
         (r';[0-9]+[.,][0-9]+ ?KM[/:. ]H$', '', True)                      ,  #sup moyenne 
         (r';(VT)([0-5])([HF]);', r';V\2\3;', False)                       ,  #modif cat Veteran 
         (r';[0-9]{1,2}[.,][0-9]{1,3}[;$]?', ';', False)                   ,  #sup moyenne 
         (r';[0-9]{5,8};', ';', False)                                     ,  #sup numero licence 
         (r'1er', '', False)                                               ,  #modif cat du type ' 1er ' 
         (r'[0-9]{1,5}eme','', False)                                      ,  #modif cat du type ' 2eme ' 
         (r' [0-9]e hom;', r';', True)                                     ,  #modif cat type '1e Hom'
         (r' [0-9]e fem;', r';', True)                                     ,  #modif cat type '1e Fem'
         (r';(SE[MF]) [0-9][0-9]*;',  r';\1;', True)                       ,  #modif cat type 'SEM 3'
         (r';(V[12345][MF]) [0-9][0-9]*;',  r';\1;', True)                 ,  #modif cat type 'V1M 3'
         (r';(ES[MF]) [0-9][0-9]*;',  r';\1;', True)                       ,  #modif cat type 'ESM 3'
         (r';(CA[MF]) [0-9][0-9]*;',  r';\1;', True)                       ,  #modif cat type 'CAM 3'
         (r';(MI[MF]) [0-9][0-9]*;',  r';\1;', True)                       ,  #modif cat type 'MIM 3'
         (r';Senior ', r';SE', True)                                       ,  #modif cat 
         (r'Senior', r'SE', True)                                          ,  #modif cat 
         (r'Homme;', r'H;', True)                                          ,  #modif cat 
         (r'Femme;', r'F;', True)                                          ,  #modif cat 
         (r';Veteran ([1234]) Homme;', r'V\1H;', True)                     ,  #modif cat 
         (r';Veteran ([1234]) Femme;', r'V\1F;', True)                     ,  #modif cat 
         (r';MAS([1-5])-H;',  r';V\1H;', True)                             ,  #modif cat 
         (r';MAS([1-5])-D;',  r';V\1F;', True)                             ,  #modif cat 
         (r';SEN-D;',  r';SEF;', True)                                     ,  #modif cat 
         (r';SEN-H;',  r';SEH;', True)                                     ,  #modif cat 
         (r';SEN-H;',  r';SEH;', True)                                     ,  #modif cat 
         (r';SEN-D;',  r';SEF;', True)                                     ,  #modif cat 
         (r';ESP-D;',  r';ESF;', True)                                     ,  #modif cat 
         (r';SEH;',  r';SEM;', True)                                       ,  #modif cat 
         (r';SEH$',  r';SEM', True)                                        ,  #modif cat 
         (r';V([12345])H;',  r';V\1M;', True)                              ,  #modif cat 
         (r';V([12345])H$',  r';V\1M', True)                               ,  #modif cat 
         #sexe
         (r';m;', ';M;', False)                                            ,  #sexe en majuscule 
         (r';m$', ';M', False)                                             ,  #sexe en majuscule 
         (r';h;', ';M;', False)                                            ,  #sexe en majuscule 
         (r';f;', ';F;', False)                                            ,  #sexe en majuscule 
         (r';f$', ';F', False)                                             ,  #sexe en majuscule 
         #temps
         (r'(;[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})(\.[0-9]+);', r'\1;', False)     ,  #mod temps 
         (r';([0-9])h', r';\1:', False)                                         ,  #mod temps type ";5h"
         (r';([0-9][0-9])h', r';\1:', False)                                    ,  #mod temps type ";10h"
         (r';([0-9]:)([0-9][0-9])m([0-9][0-9])s;', r';\1\2:\3;', True)          ,  #mod temps type '1:34m32s'
         (r"''", r'', False)                                                    ,  #temps : supp des doubles quotes type "51'27''"
         (r";([0-9][0-9])'([0-9][0-9])", r';0:\1:\2', False)                    ,  #temps : modif temps si ' et abscence heure type "51'27''"
         (r"([0-9][0-9])'([0-9][0-9])", r'\1:\2', False)                        ,  #temps : modif temps si ' et abscence heure type ":51'27"
         (r";([0-9][0-9])h([0-9][0-9])m([0-9][0-9])s;", r';\1:\2:\3;', True)    ,  #temps : type ";00h30m21s;"
         (r";([0-9][0-9])h([0-9][0-9])min([0-9][0-9])s;", r';\1:\2:\3;', True)  ,  #temps : type ";30min21s;"
         (r";([0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]) AM;", r';\1;', True)           ,  #temps : type ";3:51:58 AM;"
         (r';kmh', r';', True)                                                  ,  #suppression de type ";kmh"
         (r':([0-9][0-9])([0-9][0-9];)', r':\1;', False)                        ,  #temps du type ':5265;' 
         (r'\[.*\]', '', False)                                                 ,  #geofp1 sup des crochets type '[10500]'
         (r'\(.*\)', '', False)                                                 ,  #geofp2 sup des parentheses type '(66120)'
         (r'/$', '', False)                                                     ,  #sup de l'anti slash final
         #(r';;', ';', False)                                                   ,  #sup double point-virgule
         (r' ;', ';',  False)                                                   ,  #sup espace-point virgule type  ' ;'
         (r'; $', '',  False)                                                   ,  #sup dernier point-virgule  avec un espace '; $'
         (r';$', '',  False)                                                    ,  #sup dernier point-virgule  type ';$' (A LAISSER EN FIN DE FICHIER)
         (r'^place' , r'class', True)                                           ,  #modif entete ....avant l'application des enteteKikou
   )
