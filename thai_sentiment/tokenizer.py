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

    def __init__(self):
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
        self.removeRepeat = True
        self.stopNumber = False
        self.stopword = False
        self.removeSpaces = True
        self.minLength = 1
        self.removeNonCharacter = False
        self.case_sensitive = True
        self.ngram = (1,1)

    def normalize(self, word):
        if self.stopNumber and word.isdigit():
            return False

        if self.removeSpaces and word.isspace():
            return False

        if len(word) < self.minLength:
            return False

        if self.removeNonCharacter:
            match = re.search(u"[0-9A-Za-z\u0E00-\u0E7F]+", word)
            if not match:
                return False

        return True

    def remove_stopwords(self, wordArray):
        for dd in self.stopdict:
            try:
                if self.case_sensitive:
                    wordArray.remove(dd)
                else:
                    wordArray.remove(dd.lower())
            except ValueError:
                pass

        return wordArray

    def search_special_characters(self, characters):
        match = re.search(u"[A-Za-z\d]*", characters)
        if match.group(0):
            if not self.case_sensitive:
                return match.group(0).lower()
            else:
                return match.group(0)
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

    # Find longest matching in Trie if match return id else return -1
    def longest_matching(self, text, begin_position):
        N = len(text)
        characters = text[begin_position:N]

        # check latin words and digits
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
                # Special check for case like ๆ
                if characters[len(word_valid)] in ENDING_CHAR:
                    return characters[0:(len(word_valid) + 1)]
                else:
                    return word_valid
            except:
                return word_valid
        else:
            return -1;

    def segment_text(self, text):
        begin_position = 0
        N = len(text)
        tokens = []
        token_statuses = []
        while(begin_position < N):
            match = self.longest_matching(text, begin_position)
            if match == -1:
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

    def find_ngrams(self, input_list, n):
        return zip(*[input_list[i:] for i in range(n)])

    def tokenize(self, text):
        tokens = self.segment_text(text)
        if self.stopword:
            tokens = self.remove_stopwords(tokens)

        lastresult = []
        for x in range(self.ngram[0], self.ngram[1]+1):
            for r in self.find_ngrams(tokens, x):
                match = re.search(u"[A-Za-z\d]+", ''.join(r))
                if not match:
                    lastresult.append(''.join(r))
                else:
                    lastresult.append(' '.join(r))
        return lastresult
