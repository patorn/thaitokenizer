import pytest

from thai_sentiment import Tokenizer

def test_tokenize():
    tokenizer = Tokenizer()
    text = tokenizer.tokenize('ประเทศไทยมีบริการเทเลเท็กซ์ kbank มานานเกินกว่า 4 ปีแล้ว')
    assert text == ['ประเทศไทย', 'มี', 'บริการ', 'เท', 'เล', 'เท็กซ์', ' ', 'kbank', ' ',
                    'มา', 'นาน', 'เกิน', 'กว่า', ' ', '4', ' ', 'ปี', 'แล้ว']

