#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Created on Mon Jun 18 09:23:27 2018
    @author: alexandrabenamar
"""

######################################################
## Libraries

import nltk
from nltk.corpus import reuters, stopwords
from nltk.parse.stanford import StanfordDependencyParser
import os, string

######################################################
## Required packages

nltk.download("stopwords")
nltk.download("reuters")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

######################################################

def parse_grammar(grammar, sentence):
    """
        Grammar parsing using strings.
            x Input : grammar with nltk format
            x Output : list of grammar trees
    """
    parser = nltk.ChartParser(grammar)
    return parser.parse(sentence)

def cleaning(words, language='english'):
    """
        Stopwords and punctuation removal using a list of words.
    """
    words_clean = [word for word in words
        if word.lower() not in stopwords.words(language)]
    words_clean = [word for word in words_clean
        if word.lower() not in string.punctuation]
    return(words_clean)
