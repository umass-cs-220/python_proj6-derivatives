#import pytest
from regexp import *

# match empty make_str regex epsilon to make_str ''
def test_epsilon1():
    regex = Epsilon()
    str_to_match = ''
    res = matches(regex, str_to_match)
    assert res == True

# match empty make_str regex epsilon to make_str 'a'
def test_epsilon2():
    regex = Epsilon()
    str_to_match = 'a'
    res = matches(regex, str_to_match)
    assert res == False

# match regex x to make_str 'x'
def test_Character1():
    regex = Character('x')
    str_to_match = 'x'
    res = matches(regex, str_to_match)
    assert res == True

# match regex x to make_str 'b'
def test_Character2():
    regex = Character('x')
    str_to_match = 'b'
    res = matches(regex, str_to_match)
    assert res == False

# match regex ab to make_str 'ab'
def test_seq1():
    regex = Sequence(Character('a'), Character('b'))
    str_to_match = 'ab'
    res = matches(regex, str_to_match)
    assert res == True

# match regex ab to make_str 'ac'
def test_seq2():
    regex = Sequence(Character('a'), Character('b'))
    str_to_match = 'ac'
    res = matches(regex, str_to_match)
    assert res == False

# make_str patterns
# match regex foo to make_str 'foo'
def test_str1():
    regex = make_str('foo')
    str_to_match = 'foo'
    res = matches(regex, str_to_match)
    assert res == True

# match regex foo to make_str 'bar'

# match regex empty make_str to make_str ''

# match regex empty make_str to make_str 'd'

# match regex make_str abcabc to make_str 'abcabc'

# match regex make_str abcabc to make_str 'bcabc'

# alternation
# regex (a|b) match "b"

# regex (a|b) match "a"

# regex (a|b) match "c"

# regex (a|b) match "aa"
def test_alt4():
    regex = Alternation(Character('a'), Character('b'))
    str_to_match = 'aa'
    res = matches(regex, str_to_match)
    assert res == False

# closure
# regex a* match "a"
def test_clos1():
    regex = Closure(Character('a'))
    str_to_match = 'a'
    res = matches(regex, str_to_match)
    assert res == True

# regex a* match ""

# regex a* match "a"

# regex a* match "b"

# regex (a|b)* match ""

# regex (a|b)* match "a"

# regex (a|b)* match "b"

# regex (a|b)* match "ab"

# regex (a|b)* match "ba"

# regex (a|b)* match "baab"

# regex (a|b)* match "aaaaaaaabbbbbbbb"

# regex (abc)* match ""

# regex (abc)* match "ab"

# regex (abc)* match "abc"

# regex (abc)* match "abca"

# regex (a*|b) match ""

# regex (a*|b) match "a"

# regex (a*|b) match "b"

# regex (a*|b) match "ab"

# regex (a*|b) match "aaa"

# regex (a*|b) match "aaa"

# regex (a*|b) match "aaaabaaa"

# regex (abc)* match "abcbc"

# regex (abc)* match "abcabcabcabcabc"

# regex (abc|d)* match ""

# regex (abc|d)* match "d"

# regex (abc|d)* match "dddabcd"

# regex (abc|d|foo) match "d"

# regex (abc|d|foo) match "abc"

# regex (abc|d|foo) match "foo"

# regex (a|b)*x(b|c)qg* match "xbq"
def test_regex31():
    regex = Sequence(Closure(Alternation(Character('a'), Character('b'))),
                   Sequence(Character('x'), Sequence(Alternation(Character('b'), Character('c')),
                                               Sequence(Character('q'),
                                                  Closure(Character('g'))))))
    str_to_match = 'xbq'
    res = matches(regex, str_to_match)
    assert res == True


# regex (a|b)*x(b|c)qg* match "axbq"

# regex (a|b)*x(b|c)qg* match "xcq"

# regex (a|b)*x(b|c)qg* match "aaabbxbqggg"

# regex (a|b)*x(b|c)qg* match "abcabcccc"

# regex (a|b)*x(b|c)qg* match "abzcabcccc"

# regex (abc|c*)* match "abcabcccc"

#    python -m pytest -v testregex.py