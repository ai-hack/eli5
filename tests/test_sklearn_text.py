from sklearn.feature_extraction.text import CountVectorizer

from eli5.sklearn.text import get_weighted_spans


def test_weighted_spans_word():
    doc = 'I see: a leaning lemon tree'
    vec = CountVectorizer(analyzer='word')
    vec.fit([doc])
    w_spans = get_weighted_spans(
        doc, vec,
        {'pos': [('see', 0.2), ('lemon', 0.5), ('bias', 0.8)],
         'neg': [('tree', -0.6)]})
    assert w_spans == {
        'analyzer': 'word',
        'document': 'i see: a leaning lemon tree',
        'weighted_spans': [
            ('see', [(2, 5)], 0.2),
            ('lemon', [(17, 22)], 0.5),
            ('tree', [(23, 27)], -0.6)],
        'not_found': {'pos': [('bias', 0.8)], 'neg': []}}


def test_weighted_spans_word_bigrams():
    doc = 'I see: a leaning lemon tree'
    vec = CountVectorizer(analyzer='word', ngram_range=(1, 2))
    vec.fit([doc])
    w_spans = get_weighted_spans(
        doc, vec,
        {'pos': [('see', 0.2), ('leaning lemon', 0.5), ('lemon tree', 0.8)],
         'neg': [('tree', -0.6)]})
    assert w_spans == {
        'analyzer': 'word',
        'document': 'i see: a leaning lemon tree',
        'weighted_spans': [
            ('see', [(2, 5)], 0.2),
            ('tree', [(23, 27)], -0.6),
            ('leaning lemon', [(9, 16), (17, 22)], 0.5),
            ('lemon tree', [(17, 22), (23, 27)], 0.8)],
        'not_found': {'pos': [], 'neg': []}}


def test_weighted_spans_word_stopwords():
    doc = 'I see: a leaning lemon tree'
    vec = CountVectorizer(analyzer='word', stop_words='english')
    vec.fit([doc])
    w_spans = get_weighted_spans(
        doc, vec,
        {'pos': [('see', 0.2), ('lemon', 0.5), ('bias', 0.8)],
         'neg': [('tree', -0.6)]})
    assert w_spans == {
        'analyzer': 'word',
        'document': 'i see: a leaning lemon tree',
        'weighted_spans': [
            ('lemon', [(17, 22)], 0.5),
            ('tree', [(23, 27)], -0.6)],
        'not_found': {'pos': [('bias', 0.8), ('see', 0.2)], 'neg': []}}


def test_weighted_spans_char():
    doc = 'I see: a leaning lemon tree'
    vec = CountVectorizer(analyzer='char', ngram_range=(3, 4))
    vec.fit([doc])
    w_spans = get_weighted_spans(
        doc, vec,
        {'pos': [('see', 0.2), ('a le', 0.5), ('on ', 0.8)],
         'neg': [('lem', -0.6)]})
    assert w_spans == {
        'analyzer': 'char',
        'document': 'i see: a leaning lemon tree',
        'weighted_spans': [
            ('see', [(2, 5)], 0.2),
            ('lem', [(17, 20)], -0.6),
            ('on ', [(20, 23)], 0.8),
            ('a le', [(7, 11)], 0.5)],
        'not_found': {'pos': [], 'neg': []}}


def test_weighted_spans_char_wb():
    doc = 'I see: a leaning lemon tree'
    vec = CountVectorizer(analyzer='char_wb', ngram_range=(3, 4))
    vec.fit([doc])
    w_spans = get_weighted_spans(
        doc, vec,
        {'pos': [('see', 0.2), ('a le', 0.5), ('on ', 0.8)],
         'neg': [('lem', -0.6), (' lem', -0.4)]})
    assert w_spans == {
        'analyzer': 'char_wb',
        'document': 'i see: a leaning lemon tree',
        'weighted_spans': [
            ('see', [(2, 5)], 0.2),
            ('lem', [(17, 20)], -0.6),
            ('on ', [(20, 23)], 0.8),
            (' lem', [(16, 20)], -0.4)],
        'not_found': {'pos': [('a le', 0.5)], 'neg': []}}
