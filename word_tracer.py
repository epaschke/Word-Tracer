from collections import deque

class Tracer:
    def __init__(self, start, end, wordGenerator):
        self.queue = deque() # create queue
        self.wordsChecked = {} # hash table for words used
        self.sol = None # solution
        self.start = start # start word
        self.end = end # end word
        self.wordGenerator = wordGenerator # use same WordGenerator each time

    def startprog(self): # begin program
        if not self.wordGenerator.isWord(self.start): # if start word isn't a word
            print(self.start + " isn't in the dictionary")
        elif not self.wordGenerator.isWord(self.end): # if end word isn't a word
            print(self.end + " isn't in the dictionary")
        else: # start queue
            self.queue.append([self.start, []]) # add start word and empty array tracing word evol. to queue
            while len(self.queue) > 0 and self.sol == None:
                self.search()
            self.printSol() # when done, print solution

    def search(self): # using the queue
        cur = self.queue.popleft() # pop off queue
        if cur[0] == self.end: # if queued word is end word, set solution & end loop
            self.sol = cur if self.sol is None or self.sol[1] > cur[1] else self.sol
        elif cur[0] not in self.wordsChecked: # if queued word has not been checked already
            self.wordsChecked[cur[0]] = True  # add word to hash table
            possibilities = self.wordGenerator.generate(cur[0]) # generate array of next words to check
            for p in possibilities:
                self.queue.append([p, cur[1] + [p]]) # add each word to queue & add to array of words

    def printSol(self):
        if self.sol == None: # if program runs and finds no solution
            print("-1")
        else: # print number of words and list of them
            init = ''
            for s in self.sol[1]:
                init = init + s + " "
            print(str(len(self.sol[1])) + " words: " + init)

class WordGenerator:
    def __init__(self, dictionary):
        self.dictionary = {}
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        words = open(dictionary, 'r').readlines() # open dictionary file
        for w in words:
            word = w
            while word[-1:] not in self.alpha: # add each word from dictionary to a hash table as True
                word = word[:-1]
            self.dictionary[word] = True

    def isWord(self, word): # returns if word is in dictionary
        return self.dictionary[word] if word in self.dictionary else False

    def generate(self, word): # returns array of possible next words
        return self.switchLetter(word) + self.removeLetter(word) + self.addLetter(word)

    def removeLetter(self, word): # removes letter from current word to make a new word
        wordsArr = []
        c = 0
        while c < len(word):
            test = word[1:] if c == 0 else word[:c] + word[c + 1:] # remove 1 letter at a time from word
            if self.isWord(test): # if the test word is a word, add to array
                wordsArr.append(test)
            else: # if not a word, add to dictionary as False
                self.dictionary[test] = False
            c += 1
        return wordsArr # array of words to be tested

    def addLetter(self, word): # adds letter to current word to make a new word
        wordsArr = []
        for letter in self.alpha:
            c = 0
            while c <= len(word):
                test = letter + word if c == 0 else word[:c] + letter + word[c:] # add letter to word at each index
                if self.isWord(test): # if the test word is a word, add to array
                    wordsArr.append(test)
                else: # if not a word, add to dictionary as False
                    self.dictionary[test] = False
                c = c + 1
        return wordsArr

    def switchLetter(self, word): # switch single letter to make a new word
        wordsArr = []
        c = 0
        while c < len(word):
            each = list(word) # split word into array
            for letter in self.alpha:
                each[c] = letter # switch each letter's index with another letter from alpha array
                test = ''.join(each) # rejoin
                if test != word and self.isWord(test): # if the test word is a word, add to array
                    wordsArr.append(test)
                elif test != word: # if not a word, add to dictionary as False
                    self.dictionary[test] = False
            c = c + 1
        return wordsArr


# start
dictionary = raw_input("enter location of dictionary file: ")
wordGenerator = WordGenerator(dictionary) # create WordGenerator instance
while True: # start loop
    start = raw_input("enter first word: ")
    end = raw_input("enter end word: ")
    Tracer(start, end, wordGenerator).startprog() # init Tracer instance and start program

    playAgain = raw_input("would you like to play again? y/n: ") # play again
    if playAgain is not "y" and playAgain is not "Y": # exit loop
        break
