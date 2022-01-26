from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from string import punctuation, digits, ascii_lowercase
import pickle

stop_symb = punctuation + digits + ascii_lowercase
stemmer = SnowballStemmer("russian")
sw = stopwords.words('russian')
comm_words = pickle.load(open('model/top_common_words', 'rb'))


def custom_tokenizer(s):
    s = [stemmer.stem(word) for word in word_tokenize(s.lower()) if word not in sw and word not in comm_words and
         word.translate(str.maketrans('', '', stop_symb)) == word]
    return s
