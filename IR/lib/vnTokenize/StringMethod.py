
PUNCTUATION = [',', ':', '.', '?', '!']

def Expand(word):
    global PUNCTUATION
    _words, str = [], ''
    for i in range(0, len(word)):
        if word[i] in PUNCTUATION:
            if len(str) > 0:
                _words.append(str)
            _words.append(word[i])
            str = ''
        else:
            str += word[i]
    if len(str) > 0: _words.append(str)
    return _words

def Split(sentence):
    words = sentence.split()
    _words = []
    for word in words: _words += Expand(word)
    return _words

def Lowers(_list):
    return [word.lower() for word in _list]

def connectName(sentence):
    res, b = [], []
    words = sentence.split()
    n = len(words)
    if n == 0: return sentence
    res, i = [words[0]], 1
    while i < n:
        si, si_1 = words[i], words[i-1]
        ni, ni_1 = len(si.split('_')), len(si_1.split('_'))

        if ni == 1 and ni_1 == 1 and si[0].isupper() and si_1[0].isupper():
            res[-1] = res[-1] + '_' + words[i]
        else:
            res.append(words[i])
        i += 1
    return ' '.join(res)
