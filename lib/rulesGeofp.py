patterns = \
    (  
        (r'\[\\]', '', False )                                            ,  # tous les caracteres pourris de tabulation (tab, rc, ...)
        (r'[?"]', '', False)                                              ,  # tous les caracteres a supprimer
        (r'[éèêë]', 'e', False)                                           ,  # remplacement des accents
        (r'[ÉÈÊË]', 'E', False)                                           ,  # remplacement des accents
        (r'[C]', 'C', False)                                              ,  #remplacement des accents
        (r'[Ç]', 'C', False)                                              ,  #remplacement des accents
#        (r'^[a-bA-Z ].*$', 'ZOB', False)                                      ,  #remplacement de '; ;' par ';'
        (r'^[a-bA-Z].*$', '', False)                                      ,  #remplacement de '; ;' par ';'
        (r'^([0-9]+) ', r'\1;', False)                                    ,  #suppression des espaces en debut de ligne
        (r'\[[0-9]*\]', ';', False)                                       ,  #remplacement [9999]
        (r'\([0-9]*\)', ';', False)                                       ,  #remplacement (9999)
        (r'[0-9][0-9]\/[0-9][0-9]', ';', False)                           ,  #remplacement 01/10
        (r'[ ][ ]+', ';', False)                                          ,  #remplacement de deux espaces et plus par ';'
        (r'[;][;]+', ';', False)                                          ,  #remplacement de ';;' par ';'
        (r'; ;', ';', False)                                              ,  #remplacement de '; ;' par ';'
    )