"""
Classify data.
"""
import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import numpy as np
from sklearn.model_selection import KFold


def read_data(filename):
	""" This method reads the train/test data files and creates a list of 
	train/test data and labels.
	Args:
	  filename.... name of the file to be read.
	Returns:
	  two lists, one of data and the other with labels.
	""" 
	data = []
	labels = []
	
	file = open(filename, 'r')
	csvreader = csv.reader(file)
	for text in csvreader:
		data.append(text[0])
		labels.append(text[2])
	file.close()

	return data, labels



def vectorize(X_train, Y_train, mindf, maxdf):
	""" takes in the data, removes the stop words and converts it into a csr matrix.
	Args:
	  X_train.... training data.
	  X_test..... training labels.
	  mindf...... min_df value for the vectorizer.
	  max_df..... max_df value for the vectorizer.
	Returns:
	  csr matrix
	"""
	tfidf = TfidfVectorizer(min_df = mindf, max_df = maxdf, stop_words = 'english')
	X = tfidf.fit_transform(X_train)
	Y = tfidf.transform(Y_train)
	
	return X, Y



def classification(Y, X, X_test, Y_test):
	""" Takes in the train, test vectors and the train labels to perform classification
	using LinearRegression().
	Args:
	  Y.......csr matrix containing the vectors for test data.
	  X.......csr matrix containing the vectors for train data.
	  X_test.. list of train data labels.
	  Y_test.. list of test data labels.
	Returns:
	  list of predicted labels on the test data.
	"""
	model = LogisticRegression(solver = 'liblinear')
	model.fit(X, X_test)
	predictions = model.predict(Y)

	accuracy = accuracy_score(Y_test, predictions)
	print("Accuracy = ", accuracy)

	file = open('./Classify/classification_summary.txt', 'w')
	file.write("Accuracy = " + str(accuracy) + "\n\n")
	
	return predictions



def cross_validation(X_train, X_test, Y_train, Y_test, X, k):
	""" this method performs cross validation by combining the train and test
	data into single data list and fit the model.
	Args:
	  X_train.... list of train data.
	  X_test.... list of train labels.
	  Y_train.... list of test data.
	  Y_test.... list of test labels.
	  X......... csr matrix containing the vectors for train data.
	  k......... integer representing the number of folds of cross validation.
	Returns:
	  Nothing
	"""
	for i in range(len(Y_train)):
		X_train.append(Y_train[i])
		X_test.extend(Y_test[i])

	X_test = np.array(X_test)		

	cv = KFold(n_splits = k)
	accuracies = []

	clf = LogisticRegression(solver = 'liblinear')
	for train_idx, test_idx in cv.split(X):
		clf.fit(X[train_idx], X_test[train_idx])
		predictions = clf.predict(X[test_idx])
		accuracies.append(accuracy_score(X_test[test_idx], predictions))

	acc = np.mean(np.array(accuracies))
	print("Cross validation accuracy:", np.mean(np.array(accuracies)))
	file = open('./Classify/classification_summary.txt', 'a')
	file.write("Cross Validation Accuracy = " + str(acc) + "\n\n")



def classification_result(Y_train, predictions):
	""" writes the classification summary into a file.
	Args: 
	  Y_train...... list of test data.
	  predictions.. list of predicted labels.
	Returns:
	  Nothing
	"""
	num_neg = 0
	num_pos = 0
	neg_index = 0
	pos_index = 0

	for i in range(len(predictions)):
		if predictions[i] == str(0):
			num_neg += 1
			neg_index = i
		elif predictions[i] == str(1):
			num_pos += 1
			pos_index = i

	print("Number of Negative tweets:", num_neg)
	print("Number of Positive tweets:", num_pos)
	print("Negative tweet:", Y_train[neg_index])
	print("Positive tweet:", Y_train[pos_index])

	file = open('./Classify/classification_summary.txt', 'a')
	file.write("Number of Negative tweets: " + str(num_neg) + "\n")
	file.write("Number of Positive tweets: " + str(num_pos) + "\n\n")
	file.write("Negative tweet: " + Y_train[neg_index] + "\n")
	file.write("Positive tweet: " + Y_train[pos_index] + "\n\n")
	file.close()



def main():
	X_train, X_test = read_data("./Collect Data/train.csv")
	Y_train, Y_test = read_data("./Collect Data/test.csv")
	X, Y = vectorize(X_train, Y_train, mindf = 4, maxdf = 0.8)
	predictions = classification(Y, X, X_test, Y_test)
	cross_validation(X_train, X_test, Y_train, Y_test, X, 3)
	classification_result(Y_train, predictions)
	pass

if __name__ == "__main__":
    main()