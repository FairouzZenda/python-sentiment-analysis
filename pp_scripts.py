#   References:
#
#   http://pythonforengineers.com/intro-to-nltk-part-2/
#       - creating word features, adding True to tokens
#   https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
#       - creating reg expressions, emoji strings, tokenizer functions
#   http://www.nltk.org/book/ch06.html
#       - classifying sentiment, creating word features

# natural language toolkit
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# for regular expressions
import re
# for string operations
import string


# emoticons/emojis
# list of possible combinations
# this is used for tokenization
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

# regular expressions
# this is used for tokenization
regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @ mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]


# creates list of regular expressions
tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
# creates list of  all possile combinations for emoticons
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


# section defines my stop_words dictionary
# I have updated default stopwords english dictionary with:
#       punctuation
#       Twitter terms such as "rt", "RT", ":"
#       and also spelling errors
punctuation = list(string.punctuation)
stop_words = set(stopwords.words('english'))
stop_words.update(punctuation, ['rt', 'RT', '@', '’', '…', ':', 'cant', 'didnt', 'doesnt', 'dont', 'goes', 'isnt', 'hes', 'shes', 'thats', 'theres',
                                'theyre', 'wont', 'youll', 'youre', 'youve', 'br', 've', 're', 'vs', 'this', 'i', 'get'])


# tokenize function
# compiles a list of tokens from regular expressions
def tokenize(s):
    return tokens_re.findall(s)

# myTokenizer function


def myTokenizer(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# myFeatures function
# creates list of words not included in stop_words,
# and appends 'True' after each word for NaiveBayes


def myFeatures(words):
    useful_words = [word for word in words if word not in stop_words]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict
