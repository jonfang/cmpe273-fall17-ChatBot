import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def word_feats(words):
    return dict([(word, True) for word in words])

#set up training set
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September' 'October', 'Novemeber', 'December']
numbers = ['1','2','3','4','5','6','7','8','9','10']
intro_vocab = ['hey', 'hello', 'greetings', 'anyone']
reserve_vocab = ['reserve', 'appointment', 'make'] 
start_vocab = ['check', 'book', 'checkin'] + months
end_vocab = ['end', 'date', 'leave']
hotel_vocab = ['hotel', 'type']
room_vocab =  ['single','double','luxury']
checkout_vocab = ['name']

intro_features = [(word_feats(intro), 'intro') for intro in intro_vocab]
reserve_features = [(word_feats(reserve), 'reserve') for reserve in reserve_vocab]
start_features = [(word_feats(start), 'start') for start in start_vocab]
end_features = [(word_feats(end), 'end') for end in end_vocab]
hotel_features = [(word_feats(hotel), 'hotel') for hotel in hotel_vocab]
room_features = [(word_feats(room), 'room') for room in room_vocab]
checkout_features = [(word_feats(checkout), 'checkout') for checkout in checkout_vocab]

train_set = intro_features + reserve_features + start_features + end_features + hotel_features + room_features + checkout_features

classifier = NaiveBayesClassifier.train(train_set) 

def nl_filter(words):
    stop_words = ['I', 'want', 'would', 'like', '?', '!']
    stopWords = set(stopwords.words('english')+stop_words)
    wordsFiltered = []
    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)
    words = wordsFiltered #replace words with filtered words
    return words
 
class NLProcessor:
    """
    Natural language processor that turns input into commands
    """
    def __init__(self):
        self.intro = 0
        self.reserve = 0
        self.start = 0 
        self.end = 0
        self.hotel = 0 
        self.room = 0 
        self.checkout = 0
        self.words = ""

    def process(self, sentence):
        self.reset()
        sentence = sentence.lower()
        self.words = word_tokenize(sentence)
        self.words = nl_filter(self.words)
        #print(self.words)
        for word in self.words:
            classResult = classifier.classify(word_feats(word))
            if classResult == 'intro':
                self.intro = self.intro + 1
            if classResult == 'reserve':
                self.reserve = self.reserve + 1
            if classResult == 'start':
                self.start = self.start + 1
            if classResult == 'end':
                self.end = self.end + 1
            if classResult == 'hotel':
                self.hotel = self.hotel + 1
            if classResult == 'room':
                self.room = self.room + 1
            if classResult == 'checkout':
                self.checkout = self.checkout + 1
        #print('Intro: ' + str(float(self.intro)/len(self.words)))
        #print('Reserve: ' + str(float(self.reserve)/len(self.words)))
        #print('Start: ' + str(float(self.start)/len(self.words)))
        #print('End: ' + str(float(self.end)/len(self.words)))
        #print('Hotel: ' + str(float(self.hotel)/len(self.words)))
        #print('Room: ' + str(float(self.room)/len(self.words)))
        #print('Checkout: ' + str(float(self.checkout)/len(self.words)))
        #get probability of each command
        intro_p = float(self.intro)/len(self.words)
        reserve_p = float(self.reserve)/len(self.words)
        start_p = float(self.start)/len(self.words)
        end_p = float(self.end)/len(self.words)
        hotel_p = float(self.hotel)/len(self.words)
        room_p = float(self.room)/len(self.words)
        checkout_p = float(self.checkout)/len(self.words)
        #find out the exact command and process string accordingly
        command = "error"
        day = ""
        if checkout_p > 0:
            command = "checkout " + self.words[-1]
        elif room_p > 0:
            command = "book_room "
            for word in self.words:
                if "single" in word or "double" in word or "luxury" in word:
                    day = word
                    break
            command+=day
        elif hotel_p > 0:
            command = "book_hotel "
            for word in self.words:
                if "hotela" in word or "hotelb" in word or "hotelc" in word:
                    day = word
                    break
            command+=day
        elif end_p > 0:
            command = "set_end_date "
            for word in self.words:
                if "-" in word:
                    day = word
                    break
            command+=day
        elif start_p > 0:
            command = "set_start_date "
            for word in self.words:
                if "-" in word:
                    day = word
                    break
            command+=day
        elif reserve_p > 0:
            command = "reserve"
        else:
            command = "hi"
        return command

    def reset(self):
        self.intro = 0
        self.reserve = 0
        self.start = 0 
        self.end = 0
        self.hotel = 0 
        self.room = 0 
        self.checkout = 0
        self.words = ""

#nlp = NLProcessor()
#command = nlp.process("name is Jon")
#print(command)
