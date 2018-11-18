from pickle import load
from pickle import dump
from numpy.random import rand
from numpy.random import shuffle
from numpy import loadtxt

# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))

# save a list of clean sentences to file
def save_clean_data(sentences, filename):
	dump(sentences, open(filename, 'wb'))
	print('Saved: %s' % filename)

# load dataset
a = loadtxt('traindata6.csv', delimiter=',', dtype=str)

# reduce dataset size
n_sentences = 3224
dataset = a[:n_sentences, :]

# random shuffle
shuffle(dataset)

# split into train/test
train, test = dataset[:3224], dataset[3224:]

# save
save_clean_data(dataset, 'both.pkl')
save_clean_data(train, 'train.pkl')
save_clean_data(test, 'test.pkl')
