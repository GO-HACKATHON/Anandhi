import re

from anandhibot.preprocessing.casefolder import Casefolder
from anandhibot.preprocessing.tokenizer import Tokenizer
from anandhibot.preprocessing.stopwordremover import StopWordRemover

from anandhibot.answer import Answer
from anandhibot.cluewords import ClueWords

class AnswerFinder:
	def __init__(self, EAT, query, keywords, docs):
		stopWordRemover = StopWordRemover()

		self.EAT = EAT
		cf = Casefolder().casefold(query)
		stop = stopWordRemover.stopwordRemoval(cf)
		token = Tokenizer().tokenize(stop)
		self.pertanyaanNonStem = token
		self.pertanyaanStem = keywords
		self.keywords = keywords
		self.docs = docs
		self.maxAnswer = 5

		self.tempDoc = []


	def findWord(self, sentence, word):
		for w in word:
			if w in sentence:
				return True
		return False


	def countOccurences(self, keywords, words):
		sum = 0
		for keyword in keywords:
			sum = sum + words.count(keyword)
		return sum


	def getAnswers(self):
		answers = self.getAnswersFromDocs(self.docs)

		# sort the answers
		a = sorted(answers, key=lambda x: x.priority, reverse=True) #sort by keywordOccurence
		print (a)
		b = sorted(a, key=lambda x: x.priority) #sort by priority
		print(b)
		c = sorted(b, key=lambda x: x.pattern) #sort by pattern
		print(c)

		# group the same answers
		jawaban = []
		dict = {}

		for answer in c:
			if answer.key not in dict:
				dict[answer.key] = 1
				jawaban.append(answer.key)

		return jawaban


	def getAnswersFromDocs(self, docs):
		stopwordsRemover = StopWordRemover()

		if self.EAT == "definisi":
			clueWords = ClueWords("definisi")
			print(clueWords.afterKeywords)
		elif self.EAT == "lokasi":
			clueWords = ClueWords("lokasi")
			print(clueWords.afterKeywords)
		elif self.EAT == "prospek":
			clueWords = ClueWords("prospek")
			print(clueWords.afterKeywords)
		else:
			clueWords = ClueWords("definisi")
			print(clueWords.afterKeywords)

		print("Clueword:\n" + clueWords.clue)

		answers = []

		# iterate through all documents
		indexDocument = 0
		lenDocuments = len(docs)

		while indexDocument < lenDocuments:
			if docs[indexDocument] not in self.tempDoc:
				self.tempDoc.append(docs[indexDocument])
				print("Now at document:\n" + docs[indexDocument].url)
				# split into paragraph
				paragraphs = docs[indexDocument].content.split("\n\n")

				# iterate through all paragraphs
				for paragraph in paragraphs:
					# keyword in paragraph
					p = paragraph.lower()
					print("Now at paragraph:\n" + p)
					if self.findWord(re.split("[,]", p), self.pertanyaanStem) or self.findWord(p.split(" "), self.pertanyaanNonStem):
						# split paragraph into sentences
						sentences = re.split("[.!?][\s][1,100]", paragraph)

						prevSentence = ""

						#iterate through all sentence
						indexSentence = 0
						lenSentences = len(sentences)

						while indexSentence < lenSentences:
							s = sentences[indexSentence].lower()
							print("Now at sentence\n" + s)

							#check if keyword in sentence
							if self.findWord(re.split("[,]", p), self.pertanyaanStem) or self.findWord(s.split(" "), self.pertanyaanNonStem):
								words = Tokenizer().tokenize(Casefolder().casefold(sentences[indexSentence]))

								lenWords = len(words)
								occurence = self.countOccurences(self.pertanyaanNonStem, words)

								cluewordPosition = 0
								cluewordTipe = 0

								indexWord = 0

								while indexWord < lenWords:
									if words[indexWord] in clueWords.afterKeywords:
										print("true")
										wordsBeforeClueword = stopwordsRemover.stopwordRemoval(" ".join(words[0:indexWord]))
										wordsAfterClueword = stopwordsRemover.stopwordRemoval(" ".join(words[indexWord+1:]))
										cluewordPosition = indexWord
										cluewordTipe = 1
										indexWord = lenWords

									# print("Info:\n" + wordsBeforeClueword + wordsAfterClueword + cluewordPosition + cluewordTipe)

									indexWord = indexWord + 1

								if cluewordTipe == 1:
									keywordNonStemExist = []
									keywordStemExist = []

									indexWord = 0

									while indexWord < cluewordPosition:
										if words[indexWord] in self.pertanyaanNonStem and words[indexWord] not in keywordNonStemExist:
											keywordNonStemExist.append(words[indexWord])
										if words[indexWord] in self.pertanyaanStem and words[indexWord] not in keywordStemExist:
											keywordStemExist.append(words[indexWord])

										indexWord = indexWord + 1

									print("List keyword stem:\n" + ', '.join(keywordNonStemExist))
									print("List keyword Non stem:\n" + ', '.join(keywordNonStemExist))

									# pattern 1, priority 1
									# All non stemmed keywords + clue words + ...
									if len(keywordNonStemExist) == len(self.keywords) and len(keywordNonStemExist) == len(wordsAfterClueword):
										answers.append(Answer(indexDocument, docs[indexDocument].title, docs[indexDocument].url, sentences[indexSentence] + ".", 1, 1, occurence))
									else:
										# pattern 4, priority 2
										# One or more non-stemmed keywords + clue word + ....
										if len(keywordNonStemExist) > 0:
											answers.append(Answer(indexDocument, docs[indexDocument].title, docs[indexDocument].url, sentences[indexSentence] + ".", 4, 2, occurence))
										# pattern 7, priority 3
										# One or more stemmed keywords + clue word + ...
										if len(keywordStemExist) > 0:
											answers.append(Answer(indexDocument, docs[indexDocument].title, docs[indexDocument].url, sentences[indexSentence] + ".", 7, 3, occurence))


								# no clue in sentence
								else:
									keywordNonStemExist = []
									keywordStemExist = []

									indexWord = 0

									while indexWord < lenWords:
										if words[indexWord] in self.pertanyaanNonStem and words[indexWord] not in keywordNonStemExist:
											keywordNonStemExist.append(words[indexWord])
										if words[indexWord] in self.pertanyaanStem and words[indexWord] not in keywordStemExist:
											keywordStemExist.append(words[indexWord])

										indexWord = indexWord + 1

									print("List keyword stem:\n" + ', '.join(keywordNonStemExist))
									print("List keyword Non stem:\n" + ', '.join(keywordNonStemExist))

									# pattern 3, priority 1
									# Sentence with all non stemmed keywords. Sentence with clue word + ...
									# Try to get the first sentence
									if len(keywordNonStemExist) == len(self.keywords):
										prevSentence = sentences[indexSentence]
										prevPattern = 3
										prevPriority = 1
										prevOccurence = occurence
									else:
										# pattern 6, priority 2
										# Sentence with one or more non-stemmed keywords. Sentence with clueword + ...
										# Try to get the first sentence
										if len(keywordNonStemExist) > 0:
											prevSentence = sentences[indexSentence]
											prevPattern = 6
											prevPriority = 2
											prevOccurence = occurence

										# pattern 9, priority 3
										# Sentence with one or more stemmed keywords. Sentence with clue word + ....
										if len(keywordStemExist) > 0:
											prevSentence = sentences[indexSentence]
											prevPattern = 9
											prevPriority = 3
											prevOccurence = occurence

								# condition to check pattern 3, 6, 9
								if not cluewordPosition == 0:
									# check if there is previous sentence exist as an answer
									if not prevSentence == "":
										answers.append(Answer(indexDocument, docs[indexDocument].title, docs[indexDocument].url, prevSentence + "." + sentences[indexSentence] + ".", prevPattern, prevPriority, prevOccurence))
								else:
									# pattern 10
									# Sentence with all non stemmed keywords.
									if not prevSentence == "" and prevPattern == 3:
										answers.append(Answer(indexDocument, docs[indexDocument].title, docs[indexDocument].url, prevSentence + ".", 10, 3, prevOccurence))
									
									# pattern 11
									# Sentence with one or more non stemmed keywords
									elif not prevSentence == "" and prevPattern == 6:
										answers.append(Answer(indexDocument, docs[indexDocument].title, docs[indexDocument].url, prevSentence + ".", 11, 3, prevOccurence))

							indexSentence = indexSentence + 1

			indexDocument = indexDocument + 1

		print(answers)
		return answers