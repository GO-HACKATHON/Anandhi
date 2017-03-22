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
		keywordOfPerson = ["adalah","ialah","yaitu","nama","bernama"]
		keywordOfLocation = ["di","ke","dari","tempat"]
		keywordOfTime = ["pada","hari","minggu","tanggal","bulan","tahun","abad","jam",
						"menit","detik","januari","februari","maret","april","mei","juni",
						"juli","agustus","september","oktober","november","desember"]
		keywordOfOrganization = ["organisasi","perusahaan","badan","institusi","lembaga",
								"partai","komisi","sekolah","komite","universitas"]
		keywordOfQuantity = ["jumlah","banyak","kilo","gram","meter"]

		#keyword for non factoid question
		keywordOfDefinition = ["\"\"","''","merupakan","definisi","dimaksud","pengertian","arti",
								"disebut","dikenal","dinamakan","mendefinisikan","adalah",
								"yaitu","ialah","merujuk","diartikan"]
		keywordOfReason = ["\"\"","''","demikian","jadi","sebabnya","karenanya","maka",
							"menyebabkan","dikatakan","tujuan","terjadinya","sehingga","sebab",
							"penyebab","disebabkan","menyebabkan","karena","bertujuan",
							"terjadi"]
		keywordOfMethod = ["\"\"","''","cara","untuk","proses","langkah","tahap","tahapan"]

		#question word
		questionWords = ["siapa","siapakah","dimana","dimanakah","kemana","kemanakah","darimana",
						"darimanakah","kapan","kapankah","berapa","berapakah","apa","apakah",
						"mengapa","kenapa","bagaimana","bagaimanakah"]

		words = Casefolder().casefold(pertanyaan).split(" ")

		for word in words:
			if word in questionWords:
				if word=="siapa" or word=="siapakah":
					self.questionEAT = "person"
				elif word=="dimana" or word=="dimanakah" or word=="kemana" or word=="kemanakah" or word=="darimana" or word=="darimanakah":
					self.questionEAT = "location"
				elif word=="kapan" or word=="kapankah":
					self.questionEAT = "time"
				elif word=="berapa" or word=="berapakah":
					for word2 in words:
						if word2 in keywordOfTime:
							self.questionEAT = "time"
							break
						elif word in keywordOfQuantity:
							self.questionEAT = "quantity"
							break
						else:
							self.questionEAT = "quantity"
				elif word=="apa" or word=="apakah":
					for word2 in words:
						if word2 in keywordOfDefinition:
							self.questionEAT = "definition"
							break
						elif word2 in keywordOfReason:
							self.questionEAT = "reason"
							break
						elif word2 in keywordOfOrganization:
							self.questionEAT = "organization"
							break
						else:
							self.questionEAT = "definition"
				elif word=="mengapa" or word=="kenapa":
					self.questionEAT = "reason"
				elif word=="bagaimana" or word=="bagaimanakah":
					self.questionEAT = "method"
				else:
					if word in keywordOfDefinition:
						self.questionEAT = "definition"
					elif word in keywordOfLocation:
						self.questionEAT = "location"
					elif word in keywordOfMethod:
						self.questionEAT = "method"
					elif word in keywordOfOrganization:
						self.questionEAT = "organization"
					elif word in keywordOfPerson:
						self.questionEAT = "person"
					elif word in keywordOfQuantity:
						self.questionEAT = "quantity"
					elif word in keywordOfReason:
						self.questionEAT = "reason"
					elif word in keywordOfTime:
						self.questionEAT = "time"


	def setKeywords(self, pertanyaan):
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
			print("Stem: ")
			print(stemmer.stem(tk))
			keys.append(stemmer.stem(tk))

		self.keywords = keys