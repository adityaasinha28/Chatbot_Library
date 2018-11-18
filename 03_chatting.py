from pickle import load
from numpy import array
from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu
import pandas as pd

# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))

# fit a tokenizer
def create_tokenizer(lines):
	tokenizer = Tokenizer(char_level=False)
	tokenizer.fit_on_texts(lines)
	return tokenizer

# max sentence length
def max_length(lines):
	return max(len(line.split()) for line in lines)

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# generate target given source sequence
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)

# translate
def translate(model, tokenizer, sources):
	predicted = list()
	for i, source in enumerate(sources):
		# translate encoded source text
		source = source.reshape((1, source.shape[0]))
		translation = predict_sequence(model, all_tokenizer, source)
		print('ANSWER: %s' % (translation))
		predicted.append(translation.split())
		return translation

def retrieval(reply):
	#print("Retrieval function called")
	data=pd.read_csv('booksout.csv')
	arrtopic=data['topic']
	arrbook=data['book']
	#arrtopic=data['topic']
	
	for i in range(len(arrtopic)):
	    arrtopic[i]=arrtopic[i].lower()
	arrbook=data['book']
	replsplit=reply.split()
	
	topics=["networks","software engineering","theory of computation","information systems","information security","computer architecture","signal processing","logic in computer science","database systems","machine learning","artificial intelligence","algorithm design"]
	for topicvals in topics:
		topic=topicvals.split()
		#print("topic 0 is", topic[0])
	#topic=arrtopic[0].split();
		if topic[0].lower() in replsplit:
		    #print('found')
		    print('ANSWER: The following options are available:\n\n')
		    for i in range(len(arrtopic)):
		        if (arrtopic[i].split())[0]==topic[0]:
		            print("       ", arrbook[i])
	print("ANSWER: Would you like to borrow any of these books?")
	while(True):
		q=(input(str("YOU: ")))
		if( q!=None and ((q.split())[0]=='yes' or (q.split())[0]=='sure' or (q.split())[0]=='alright') ):
			print("ANSWER: The book has been issued. Thanks for using")
			break
		else:
			print("ANSWER: Query completed. Thanks for using")
			break




# load datasets
dataset = load_clean_sentences('both.pkl')
dataset1=dataset.reshape(-1,1)

# prepare tokenizer
all_tokenizer = create_tokenizer(dataset1[:,0])
all_vocab_size = len(all_tokenizer.word_index) + 1
all_length = max_length(dataset1[:, 0])

# load model
model = load_model('model2.h5')

print("\n")

# Setting up the chat
while(True):
    q = (input(str("YOU: ")))
    #reply=""
    if q == 'bye' or q=='sure' or q=='alright' or q=='waiting' or q== '<SILENCE>' or q=='silence':
        #print("Last verse was:", reply)
        retrieval(reply)
        break
    q = q.strip().split('\n')

    #we tokenize
    X = all_tokenizer.texts_to_sequences(q)
    X = pad_sequences(X, maxlen=all_length, padding='post')
        
    # find reply and print it out
    reply = translate(model, all_tokenizer, X)
    

