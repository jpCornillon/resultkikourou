#
# -*- coding: utf8
import re
#


class ApplyRegex(object):
    '''Application d'une suite de regex issu du fichier de rules passé au constructeur'''

    def __init__(self, rules):
        self.rules = rules

    # genreration des rules
    def genRules(self):
        '''generation des fonctions avec les rules(regexp) du fichier rulesKikourou'''
        for search, replace, flag in self.rules:
            if flag:
                yield lambda word: re.sub(search, replace, word, flags=re.IGNORECASE)
            else:
                yield lambda word: re.sub(search, replace, word)

    # generation/execution des rules
    # def genAndApplyRules(self, word):
    #     '''generation et execution des fonctions lamda'''
    #     for applyRule in self.genRules():
    #         word = applyRule(word)
    #     return word

    def __call__(self, word):
        '''generation et execution des fonctions lamda
           Ps : la fonction call est appelée automagiquement
           lors de l'instanciation de la classe (après init)'''
        for applyRule in self.genRules():
            # print('applyRule : {}'.format(applyRule))
            word = applyRule(word)
        return word
