def word_count(s):
    return dict((word, s.split().count(word)) for word in set(s.split()))
