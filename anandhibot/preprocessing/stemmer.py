# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Stemmer:
	def stem(self, string):
		# create stemmer
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		output = stemmer.stem(string)
		return output
