import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
ps = PorterStemmer()

nb_model = pickle.load(open('nb_model.pkl', 'rb'))
svc_model = pickle.load(open('svc_model.pkl', 'rb'))
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))

def rule_based_spam_check(text):
    text = text.lower()
    spam_phrases = [
        'click link', 'free recharge', 'limited offer',
        'claim now', 'winner', 'prize', 'lottery',
        'need your help', 'tried reaching you',
        'something important', 'check this out'
    ]
    for phrase in spam_phrases:
        if phrase in text:
            return 1
    return 0

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

def is_scam(message):
    if rule_based_spam_check(message) == 1:
        return True

    transform_sms = transform_text(message)
    vector_input = tfidf.transform([transform_sms])

    nb_pred = nb_model.predict(vector_input)[0]
    svc_pred = svc_model.predict(vector_input)[0]

    return nb_pred == 1 or svc_pred == 1

