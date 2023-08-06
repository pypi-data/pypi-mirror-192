from collections import defaultdict
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
import re
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.utils import simple_preprocess
import string

stop_words = list(set(stopwords.words('english')))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[{}0-9]'.format(string.punctuation), ' ', text)
    text=re.sub(r'[^A-Za-z0-9 ]+', ' ', text)
    text = word_tokenize(text)
    text = [word for word in text if word not in stop_words]
    text = [WordNetLemmatizer().lemmatize(word) for word in text]
    text = ' '.join(text)
    return text


def preprocess_docs(docs):
    return [preprocess_text(doc) for doc in docs]

def get_bigrammer(cleaned_docs,threshold=10):
    tokens = [simple_preprocess(string) for string in cleaned_docs]
    bigram = Phrases(tokens, min_count=2, threshold=threshold)
    bigram_phraser = Phraser(bigram)
    tokens = [bigram_phraser[t] for t in tokens]
    return tokens

def token_frequency_filter(documents_tokens,threshold=5):
    frequency = defaultdict(int)
    for document_tokens in documents_tokens:
        for token in document_tokens:
            frequency[token] += 1
    tokens = [[token for token in document_tokens if frequency[token] > threshold] for document_tokens in documents_tokens]
    return tokens