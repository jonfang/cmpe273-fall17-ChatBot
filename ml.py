import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
 
def word_feats(words):
    return dict([(word, True) for word in words])

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September' 'October', 'Novemeber', 'December']
numbers = ['1','2','3','4','5','6','7','8','9','10']

sentence = 'hello'
intro_vocab = ['hey', 'hello', 'greetings', 'anyone']
reserve_vocab = ['reserve', 'appointment', 'make'] 
start_vocab = ['check', 'book', 'checkin'] + months
end_vocab = ['end', 'date', 'leave']
hotel_vocab = ['hotel', 'type']
room_vocab =  ['single','double','luxury']
checkout_vocab = ['done']

intro_features = [(word_feats(intro), 'intro') for intro in intro_vocab]
reserve_features = [(word_feats(reserve), 'reserve') for reserve in reserve_vocab]
start_features = [(word_feats(start), 'start') for start in start_vocab]
end_features = [(word_feats(end), 'end') for end in end_vocab]
hotel_features = [(word_feats(hotel), 'hotel') for hotel in hotel_vocab]
room_features = [(word_feats(room), 'room') for room in room_vocab]
checkout_features = [(word_feats(checkout), 'checkout') for checkout in checkout_vocab]

stop_words = ['I', 'want', 'would', 'like', '?', '!']

train_set = intro_features + reserve_features + start_features + end_features + hotel_features + room_features + checkout_features

classifier = NaiveBayesClassifier.train(train_set) 
 
# Predict
intro = 0
reserve = 0
start = 0 
end = 0
hotel = 0 
room = 0 
checkout = 0
#sentence = "I would like to book a hotel"
#sentence = sentence.lower()
words = word_tokenize(sentence)
#words = sentence.split(' ')
#print(words)
#filter words
stopWords = set(stopwords.words('english')+stop_words)
wordsFiltered = []
for w in words:
    if w not in stopWords:
        wordsFiltered.append(w)
print(wordsFiltered)
words = wordsFiltered #replace words with filtered words

for word in words:
    classResult = classifier.classify( word_feats(word))
    if classResult == 'intro':
        intro = intro + 1
    if classResult == 'reserve':
        reserve = reserve + 1
    if classResult == 'start':
        start = start + 1
    if classResult == 'end':
        end = end + 1
    if classResult == 'hotel':
        hotel = hotel + 1
    if classResult == 'room':
        room = room + 1
    if classResult == 'checkout':
        checkout = checkout + 1

print('Intro: ' + str(float(intro)/len(words)))
print('Reserve: ' + str(float(reserve)/len(words)))
print('Start: ' + str(float(start)/len(words)))
print('End: ' + str(float(end)/len(words)))
print('Hotel: ' + str(float(hotel)/len(words)))
print('Room: ' + str(float(room)/len(words)))
print('Checkout: ' + str(float(checkout)/len(words)))


#iterare to find the largest and *latest in the stage
