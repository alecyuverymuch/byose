"""Part 3 solutions. See part3.py for function docstrings.

(!!!) DO NOT CHANGE ANY CODE IN THIS FILE. (!!!)
"""
import operator
import itertools
import numpy as np

from corpus import Corpus

def train_ls_classifier(A, y):
    w = np.zeros((A.shape[1], 1))
    num_iterations = 10000
    learning_rate = 0.001
    regularization_weight = 0.01
    for i in range(num_iterations):
        z = w - learning_rate * A.transpose() * (A * w - y)
        w = (1/(1 + learning_rate * regularization_weight)) * z
    return w

def train_svm_classifier(A, y):
    w = np.zeros((A.shape[1], 1))
    num_iterations = 10000
    learning_rate = 0.001
    regularization_weight = 0.01
    for i in range(num_iterations):
        # Compute the gradient.
        grad = np.zeros((A.shape[1], 1))
        for i in range(A.shape[0]):
            if y[i] * A[i] * w < 1:
                grad -= y[i, 0] * A[i, :].transpose()
        grad -= regularization_weight * 2 * w
        # Update the weight vector.
        w = w - learning_rate * grad
    return w

def classification_error(A, w, y):
    return np.sum(0.5 * (np.sign(A * w) - y))

def train_one_vs_one_classifier(category_train_documents):
    category_classifiers = []
    for cat_1, cat_2 in itertools.combinations(category_train_documents.keys(), 2):
        print 'Now training classifier for', cat_1, 'and', cat_2
        train_1 = category_train_documents[cat_1]
        train_2 = category_train_documents[cat_2]
        A = np.concatenate((train_1, train_2))
        y = np.concatenate((np.ones((train_1.shape[0], 1)),
                            -np.ones((train_2.shape[0], 1))))
        category_classifiers.append((train_svm_classifier(A, y), cat_1, cat_2))
    return category_classifiers

def classify(one_vs_one_classifiers, doc):
    votes = {}
    for tup in one_vs_one_classifiers:
        classifier = tup[0]
        cat_1 = tup[1]
        cat_1 = tup[2]
        prediction = np.sign(np.inner(doc, classifier)[0])
        if prediction == 1:
            votes[cat_1] = 0 if cat_1 not in votes else votes[cat_1] + 1
        else:
            votes[cat_2] = 0 if cat_2 not in votes else votes[cat_2] + 1
    best = sorted(votes.items(), key=operator.itemgetter(1), reverse=True)
    return (best[0][0], best[1][0])

def test_ls_classifier(corp):
    print 'Testing LS classifier on coconut vs. copper...'
    test_classifier_on_categories('money-fx', 'acq', train_ls_classifier, corp)

    print 'Testing LS classifier on coconut vs. coconut-oil...'
    test_classifier_on_categories('money-fx', 'money-supply', train_ls_classifier, corp)

def test_svm_classifier(corp):
    print 'Testing LS classifier on coconut vs. copper...'
    test_classifier_on_categories('money-fx', 'acq', train_svm_classifier, corp)

    print 'Testing LS classifier on coconut vs. coconut-oil...'
    test_classifier_on_categories('money-fx', 'money-supply', train_svm_classifier, corp)

def test_classifier_on_categories(category_1, category_2, train_classifier, corp):
    train_matrix_1 = corpus.train_matrix(category_1)
    train_matrix_2 = corpus.train_matrix(category_2)
    train_doc_matrix = np.concatenate((train_matrix_1, train_matrix_2))
    train_labels = np.concatenate((
        np.ones((train_matrix_1.shape[0], 1)),
        -np.ones((train_matrix_2.shape[0], 1))
    ))
    classifier = train_classifier(train_doc_matrix, train_labels)
    test_matrix_1 = corpus.test_matrix(category_1)
    test_matrix_2 = corpus.test_matrix(category_2)
    test_doc_matrix = np.concatenate((test_matrix_1, test_matrix_2))
    test_labels = np.concatenate((
        np.ones((test_matrix_1.shape[0], 1)),
        -np.ones((test_matrix_2.shape[0], 1))
    ))
    error = classification_error(test_doc_matrix, classifier, test_labels)
    print category_1, 'vs.', category_2, 'error:', error

if __name__ == '__main__':
    corp = Corpus()
    print 'Testing LS classifier!'
    test_ls_classifier(corp)
    print 'Testing SVM classifier!'
    test_svm_classifier(corp)
