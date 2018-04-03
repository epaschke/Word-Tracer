from collections import deque

class Setup:
    def __init__(self, start, end, dictionary):
        self.queue = deque()
        self.wordsChecked = {}
        self.sol = None
        self.start = start
        self.end = end
        self.wordGenerator = WordGenerator(dictionary)

    def startprog(self):
        if not self.wordGenerator.isWord(self.start):
            print(self.start + " isn't in the dictionary")
        elif not self.wordGenerator.isWord(self.end):
            print(self.end + " isn't in the dictionary")
        else:
            self.queue.append([self.start, 0, []])
            while len(self.queue) > 0 and self.sol == None:
                self.search()

        if self.sol == None:
            print("-1")
        else:
            print(str(self.sol[1]))
            init = ''
            for s in self.sol[2]:
                init = init + s + " "
            print(init)

    def search(self):
        cur = self.queue.popleft()
        if cur[0] == self.end:
            self.sol = cur if self.sol is None or self.sol[1] > cur[1] else self.sol
        elif cur[0] not in self.wordsChecked:
            self.wordsChecked[cur[0]] = True
            possibilities = self.wordGenerator.generate(cur[0])
            for p in possibilities:
                self.queue.append([p, cur[1] + 1, cur[2] + [p]])

class WordGenerator:
    def __init__(self, dictionary):
        self.dictionary = {}
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        words = open(dictionary, 'r').readlines()
        for w in words:
            word = w
            while word[-1:] not in self.alpha:
                word = word[:-1]
            self.dictionary[word] = True

    def isWord(self, word):
        return word in self.dictionary

    def generate(self, word):
        return self.switchLetter(word) + self.removeLetter(word) + self.addLetter(word)

    def removeLetter(self, word):
        wordsArr = []
        c = 0
        while c < len(word):
            test = word[1:] if c == 0 else word[:c] + word[c + 1:]
            if self.isWord(test):
                wordsArr.append(test)
            c += 1
        return wordsArr

    def addLetter(self, word):
        wordsArr = []
        for letter in self.alpha:
            c = 0
            while c <= len(word):
                test = letter + word if c == 0 else word[:c] + letter + word[c:]
                if self.isWord(test):
                    wordsArr.append(test)
                c = c + 1
        return wordsArr

    def switchLetter(self, word):
        wordsArr = []
        c = 0
        while c < len(word):
            each = list(word)
            for letter in self.alpha:
                each[c] = letter
                test = ''.join(each)
                if test != word and self.isWord(test):
                    wordsArr.append(test)
            c = c + 1
        return wordsArr

dictionary = raw_input("enter location of dictionary file: ")
while True:
    start = raw_input("enter first word: ")
    end = raw_input("enter end word: ")
    Setup(start, end, dictionary).startprog()

    playAgain = raw_input("would you like to play again? y/n: ")
    if playAgain is not "y" and playAgain is not "Y":
        break
