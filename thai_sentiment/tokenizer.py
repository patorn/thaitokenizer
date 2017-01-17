import re
import os
import glob
import pdb

import marisa_trie

REPO_DIR = os.getenv('data', '.')
DICTIONARY_PATH = '{0}/data/tokenizer/dict/'.format(REPO_DIR)
NEGATION_PATH = '{0}/data/tokenizer/negation.txt'.format(REPO_DIR)
STOPWORD_PATH = '{0}/data/tokenizer/stopword.txt'.format(REPO_DIR)

FRONT_DEP_CHAR = ['ะ', 'ั', 'า ', 'ำ', 'ิ', 'ี', 'ึ', 'ื', 'ุ', 'ู', 'ๅ', '็', '์', 'ํ']
REAR_DEP_CHAR = ['ั', 'ื', 'เ', 'แ', 'โ', 'ใ', 'ไ', 'ํ']
TONAL_CHAR = ['่', '้', '๊', '๋']
ENDING_CHAR = ['ๆ', 'ฯ']

class Tokenizer(object):

    def __init__(self, remove_stopword=False):
        self.dictionary = []
        self.negation_dictionary = []
        self.stopdict = []

        for file in os.listdir(DICTIONARY_PATH):
            if file.endswith('.txt'):
              with open(DICTIONARY_PATH + file) as file:
                  for line in file:
                      self.dictionary.append(line.rstrip())

        with open(NEGATION_PATH) as file:
            for line in file:
                self.negation_dictionary.append(line.rstrip())

        with open(STOPWORD_PATH) as file:
            for line in file:
                self.stopdict.append(line.rstrip())

        self.trie = marisa_trie.Trie(self.dictionary)
        self.remove_stopword = remove_stopword

    def normalize(self, word):
        # remove repeat
        # remove space
        # remove special characters
        return True

    def remove_stopwords(self, tokens):
        for stopword in self.stopdict:
            try:
                tokens.remove(stopword.lower())
            except ValueError:
                pass
        return tokens

    def search_special_characters(self, characters):
        match = re.search(u"[A-Za-z\d]*", characters)
        if match.group(0):
            return match.group(0).lower()
        else:
            return None

    def is_next_word_valid(self, text, begin_position):
        N = len(text)
        characters = text[begin_position:N].strip()

        if len(characters) == 0:
            return True

        match = self.search_special_characters(characters)
        if match:
            return True

        for position in range(N):
            if characters[0:position] in self.trie:
                return True

        return False

    def longest_matching(self, text, begin_position):
        N = len(text)
        characters = text[begin_position:N]

        match = self.search_special_characters(characters)
        if match:
            return match

        word = None
        word_valid = None

        for position in range(N):
            if characters[0:position] in self.trie:
                word = characters[0:position]
                if self.is_next_word_valid(characters, position):
                    word_valid = characters[0:position]

        if word:
            if not word_valid:
                word_valid = word

            try:
                if characters[len(word_valid)] in ENDING_CHAR:
                    return characters[0:(len(word_valid) + 1)]
                else:
                    return word_valid
            except:
                return word_valid
        else:
            return '';

    def segment_text(self, text):
        begin_position = 0
        N = len(text)
        tokens = []
        token_statuses = []
        while(begin_position < N):
            match = self.longest_matching(text, begin_position)
            if not match:
                if not text[begin_position].isspace() \
                    and (text[begin_position] in FRONT_DEP_CHAR \
                    or text[begin_position - 1] in REAR_DEP_CHAR \
                    or text[begin_position] in TONAL_CHAR \
                    or (token_statuses and token_statuses[-1] == 'unknown')):
                    tokens[-1] += text[begin_position]
                    token_statuses[-1] = 'unknown'
                else:
                    tokens.append(text[begin_position])
                    token_statuses.append('unknown')
                begin_position += 1
            else:
                if text[begin_position - 1] in REAR_DEP_CHAR:
                    tokens[-1] += match
                else:
                    tokens.append(match)
                    token_statuses.append('known')
                begin_position += len(match)

        return tokens;

    def tokenize(self, text):
        tokens = self.segment_text(text)

        if self.remove_stopword:
            tokens = self.remove_stopwords(tokens)

        return tokens
