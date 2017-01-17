import pytest

from thai_sentiment import Tokenizer

tokenizer = Tokenizer()

def test_tokenize():
    assert tokenizer.tokenize("ประเทศไทยมีบริการเทเลเท็กซ์ kbank มานานเกินกว่า 4 ปีแล้ว") == [
            'ประเทศไทย', 'มี', 'บริการ', 'เท', 'เล', 'เท็กซ์', ' ', 'kbank', ' ', 'มา', 'นาน', 'เกิน',
            'กว่า', ' ', '4', ' ', 'ปี', 'แล้ว']

def test_search_special_characters():
    assert tokenizer.search_special_characters("kbank") == 'kbank'

def test_is_next_word_valid():
    assert tokenizer.is_next_word_valid("ไทยมี", 0) == True

def test_longest_matching():
    assert tokenizer.longest_matching("ประเทศไทย", 0) == 'ประเทศ'

def test_longest_matching_of_special_characters():
    assert tokenizer.longest_matching("อื่นๆ", 0) == 'อื่นๆ'

def test_remove_stopwords():
    assert tokenizer.remove_stopwords(["เรา", "จะ", "ทำ"]) == ["ทำ"]
