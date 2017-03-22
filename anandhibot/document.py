from __future__ import division
from collections import OrderedDict

class Document:
	def __init__(self, index=0, title="", url="", content=""):
		self.index = index
		self.title = title
		self.url = url
		self.content = content

		self.words = []
		self.wordCount = OrderedDict()

	def count(self):
		return len(self.words)

	def addWord(self, word):
		self.words.append(word)

		if word in self.wordCount:
			self.wordCount[word] = self.wordCount + 1
		else:
			self.wordCount = 1

	def containWord(self, word):
		return self.wordCount.has_key(word)

	def termFrequency(self, word):
		if word not in self.wordCount:
			return float(0 / len(self.words))
		else:
			return float(self.wordCount[word] / len(self.words))