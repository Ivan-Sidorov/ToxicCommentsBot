from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from string import punctuation, digits

stop_symb = punctuation + digits
stemmer = SnowballStemmer("russian")
sw = stopwords.words('russian')


def custom_tokenizer(s):
    s = [stemmer.stem(word) for word in word_tokenize(s.lower()) if word not in sw and word.translate(str.maketrans('', '', stop_symb)) == word]
    return s
