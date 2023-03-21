from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import train_test_split


def apply_ensembling(training_set_x, training_set_y, test_set_x, test_set_y):
    X = vectorizer.fit_transform(training_set_x).toarray()
    tfidf_vect_ngram.fit(training_set_x)
    xtrain_tfidf = tfidf_vect_ngram.transform(training_set_x)
    xvalid_tfidf = tfidf_vect_ngram.transform(test_set_x)
    estimators = []
    model0 = LogisticRegression()

    model1 = RandomForestClassifier(n_estimators=500,
                                 max_features=0.25,
                                 criterion="entropy",
                                 class_weight="balanced")

    estimators.append(('lgr', model0))
    estimators.append(('rf', model1))
    model2 = DecisionTreeClassifier()
    estimators.append(('cart', model2))
    model3 = SVC()
    estimators.append(('svc', model3))

    ensemble = VotingClassifier(estimators, weights=[1, 2, 2, 1])
    ensemble.fit(X, training_set_y)
    pred = ensemble.predict(vectorizer.transform(test_set_x).toarray())
    accuracy = metrics.accuracy_score(test_set_y, pred)
    precisions, recall, f1_score, _ = metrics.precision_recall_fscore_support(test_set_y, pred)
   
    ensemble.fit(xtrain_tfidf, training_set_y)
    pred = ensemble.predict(xvalid_tfidf)
    accuracy = metrics.accuracy_score(test_set_y, pred)
    precisions, recall, f1_score, _ = metrics.precision_recall_fscore_support(test_set_y, pred)
   
    text_clf = Pipeline(
        [('vect', vectorizer), ('tfidf', TfidfTransformer()), ('vt', VotingClassifier(estimators, weights=[1, 2, 2, 1]))])

    text_clf.fit(training_set_x, training_set_y)
    pred = text_clf.predict(test_set_x)
    accuracy = metrics.accuracy_score(test_set_y, pred)
    precisions, recall, f1_score, _ = metrics.precision_recall_fscore_support(test_set_y, pred)
    