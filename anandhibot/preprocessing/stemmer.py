# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Stemmer:
	def stem(self, string):
		# create stemmer
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		output = stemmer.stem(string)
		return output
		# stemming process
		# sentence = 'Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan'
		# output   = stemmer.stem(sentence)

		# print(output)
		# # ekonomi indonesia sedang dalam tumbuh yang bangga

		# print(stemmer.stem('Mereka meniru-nirukannya'))
		# # mereka tiru
