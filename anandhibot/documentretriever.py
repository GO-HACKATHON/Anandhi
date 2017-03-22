from anandhibot.preprocessing.casefolder import Casefolder
from anandhibot.document import Document
import unicodedata

class DocumentRetriever:
	def __init__(self):
		self.documents = []
		self.urldocuments = []

	def retrieve(self, keywords):
		tempDoc = []

		with open("anandhibot/stopwords.txt", "rb") as f:
			for line in f:
				stopwords = line.split(" ")

		i = 1
		j = 1

		while i <62:
			with open("anandhibot/Data/%s.txt" % (str(i)), "rb") as d:
				for baris in d:
					filehandler = baris.decode('ascii','ignore')

			for word in keywords:
				if word in filehandler.lower():
					if i not in tempDoc:
						tempDoc.append(i)

						judul = filehandler.split(".\n")[0]
						document = Document(j, judul,  "anandhibot/Data/%s.txt" % (str(i)), filehandler)
						url = "carolapp/Data/%s.txt" % (str(i))
						self.documents.append(document)
						self.urldocuments.append(url)

						j = j + 1

			i = i + 1

		return self.urldocuments