from anandhibot.preprocessing.casefolder import Casefolder
from anandhibot.preprocessing.tokenizer import Tokenizer
from anandhibot.preprocessing.stopwordremover import StopWordRemover
from anandhibot.preprocessing.stemmer import Stemmer

class QuestionAnalyzer:
	"""docstring for QuestionAnalyzer"""
	def __init__(self):
		self.query = ""
		self.questionEAT = "undefined"
		self.keywords = None

	def __init__(self, pertanyaan):
		self.query = pertanyaan
		self.setQuestionEAT(pertanyaan)
		self.setKeywords(pertanyaan)
		
	def setQuestionEAT(self, pertanyaan):
		self.questionEAT = "undefined"

		#keyword for factoid question
		keywordOfLocation = ["di","ke","dari","tempat","kampus","kuliah","universitas","politeknik","sekolah","letak","terletak","lokasi"]
		keywordOfProspect = ["kerja","prospek","tamat","lulus"]

		#keyword for non factoid question
		keywordOfDefinition = ["\"\"","''","merupakan","definisi","dimaksud","pengertian","arti",
								"disebut","dikenal","dinamakan","mendefinisikan","adalah",
								"yaitu","ialah","merujuk","diartikan"]

		#question word
		questionWords = ["dimana","dimanakah","kemana","kemanakah","darimana","darimanakah","apa","apakah"]

		words = Casefolder().casefold(pertanyaan).split(" ")

		for word in words:
			if word in questionWords:
				if word=="dimana" or word=="dimanakah" or word=="kemana" or word=="kemanakah":
					for word2 in words:
						if word2 in keywordOfLocation:
							self.questionEAT = "lokasi"
							break
						elif word in keywordOfProspect:
							self.questionEAT = "prospek"
							break
						else:
							self.questionEAT = "lokasi"
				elif word=="apa" or word=="apakah":
					for word2 in words:
						if word2 in keywordOfDefinition:
							self.questionEAT = "definisi"
							break
						elif word2 in keywordOfProspect:
							self.questionEAT = "prospek"
							break
						else:
							self.questionEAT = "definisi"
				else:
					if word in keywordOfDefinition:
						self.questionEAT = "definisi"
					elif word in keywordOfLocation:
						self.questionEAT = "lokasi"
					elif word in keywordOfMethod:
						self.questionEAT = "prospek"


	def setKeywords(self, pertanyaan):
		#question word
		questionWords = ["dimana","dimanakah","kemana","kemanakah","darimana","darimanakah","apa","apakah","mana"]
		#keyword for factoid question
		keywordOfLocation = ["di","ke","dari","tempat","kampus","kuliah","universitas","politeknik","sekolah","letak","terletak","lokasi"]
		keywordOfProspect = ["kerja","prospek","tamat","lulus"]

		#keyword for non factoid question
		keywordOfDefinition = ["\"\"","''","merupakan","definisi","dimaksud","pengertian","arti",
								"disebut","dikenal","dinamakan","mendefinisikan","adalah",
								"yaitu","ialah","merujuk","diartikan"]
		k = ""
		keys = []
		stemmer = Stemmer()
		stopWordRemover = StopWordRemover()
		cf = Casefolder().casefold(pertanyaan)
		print("Casefolding: ")
		print(cf)
		stop = stopWordRemover.stopwordRemoval(cf)
		print("Stopword: ")
		print(stop)
		token = Tokenizer().tokenize(stop)
		print("Token: ")
		print(token)

		for tk in token:
			st = stemmer.stem(tk)
			print("Stem: ")
			print(st)
			if st not in questionWords and st not in keywordOfDefinition and st not in keywordOfProspect and st not in keywordOfLocation:
				k = k + " " + st
				
		keys.append(k[1:])

		self.keywords = keys