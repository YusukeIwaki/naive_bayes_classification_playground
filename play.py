# -*- coding:utf-8 -*-

import MeCab
import math

class Category:
    def __init__(self):
        self.totalWordCount = 0
        self.wordCount = {}

    def addWord(self, word, count):
        self.totalWordCount += count
        if word in self.wordCount:
            self.wordCount[word] += count
        else:
            self.wordCount[word] = count

class WordCounter:
    def __init__(self):
        self.mecab_tagger = MeCab.Tagger('')

    def parse(self, text):
        wordCount = {}
        tokens = [[chunk.split('\t')[0], tuple(chunk.split('\t')[1].split(','))] for chunk in self.mecab_tagger.parse(text).splitlines()[:-1]]
        for token in tokens:
            if token[1][0] == '名詞' and (token[1][1] == '一般' or token[1][1] == '固有名詞'):
                word = token[0]
                if word in wordCount:
                    wordCount[word] += 1
                else:
                    wordCount[word] = 1
        return wordCount
        

class TotalWordCounter:
    def __init__(self):
        self.count = {}

    def add(self, word):
        if word not in self.count:
            self.count[word] = 1

    def totalCount(self):
        return len(self.count.keys())

class Filter:
    def __init__(self):
        self.totalDocCount = 0
        self.categoryDocCount = {}
        self.categories = {}
        self.totalWordCounter = TotalWordCounter()
        self.wordCounter = WordCounter()

    def addDocument(self, text, categoryName):
        if categoryName not in self.categories:
            self.categories[categoryName] = Category()

        if categoryName in self.categoryDocCount:
            self.categoryDocCount[categoryName] += 1
        else:
            self.categoryDocCount[categoryName] = 1
        self.totalDocCount += 1

        for word, count in self.wordCounter.parse(text).items():
            self.totalWordCounter.add(word)
            self.categories[categoryName].addWord(word, count)

    def findCategory(self, text):
        wordCount = self.wordCounter.parse(text)
        totalWordCount = self.totalWordCounter.totalCount()
        
        probabilities = {}
        for categoryName, category in self.categories.items():
            loggedCategoryProbability = math.log(1.0 * self.categoryDocCount[categoryName] / self.totalDocCount)

            for word, count in wordCount.items():
                categoryWordCount = 0
                if word in category.wordCount:
                    categoryWordCount = category.wordCount[word]
                loggedCategoryProbability += (count * math.log(1.0 * (categoryWordCount + 1) / (category.totalWordCount + totalWordCount)))
            
            probabilities[categoryName] = loggedCategoryProbability
        
        for categoryName, value in probabilities.items():
            print("%s => %f"%(categoryName, value))
        
        

from glob import glob

f=Filter()
for filename in sorted(glob("./smap*")):
    print("Learning %s"%(filename,))
    text = open(filename, "r").read()
    f.addDocument(text, "SMAP")

for filename in sorted(glob("./tokio*")):
    print("Learning %s"%(filename,))
    text = open(filename, "r").read()
    f.addDocument(text, "TOKIO")

text = open("test", "r").read()
f.findCategory(text)
