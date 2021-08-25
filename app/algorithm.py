import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import precision_score, accuracy_score, recall_score
from database import SessionLocal
from models import AlgorithmModel
from celery import Celery


celery = Celery(
    'algorithm',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
)


def create_data():
    db = SessionLocal()
    query = db.query(AlgorithmModel)
    text = [data.text for data in query]
    label = [data.label for data in query]
    return text, label


#feature extraction - creating a tf-idf matrix
def tfidf(data, ma = 0.6, mi = 0.0001):
    tfidf_vectorize = TfidfVectorizer()
    tfidf_data = tfidf_vectorize.fit_transform(data)
    return tfidf_data, tfidf_vectorize


#SVM classifier
def test_SVM(x_train, x_test, y_train, y_test):
    SVM = SVC(kernel = 'linear', probability=True)
    SVMClassifier = SVM.fit(x_train, y_train)
    predictions = SVMClassifier.predict(x_test)
    a = accuracy_score(y_test, predictions)
    p = precision_score(y_test, predictions, average = 'weighted')
    r = recall_score(y_test, predictions, average = 'weighted')
    return SVMClassifier, a, p, r



def dump_model(model, file_output):
    pickle.dump(model, open(file_output, 'wb'))

def load_model(file_input):
    return pickle.load(open(file_input, 'rb'))


@celery.task(bind=True)
def train_service(self): 
    text, label = create_data()
    training, vectorizer = tfidf(text)
    x_train, x_test, y_train, y_test = train_test_split(training, label, test_size = 0.25, random_state = 0)
    model, accuracy, precision, recall = test_SVM(x_train, x_test, y_train, y_test)
    dump_model(model, 'model.pickle')
    dump_model(vectorizer, 'vectorizer.pickle')


def prediction_service(text):
    model = load_model('model.pickle')
    vectorizer = load_model('vectorizer.pickle')
    tdifd = vectorizer.transform([text])
    result = model.predict_proba(tdifd)
    return result