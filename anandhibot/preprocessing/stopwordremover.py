import unicodedata
import re 
class StopWordRemover:
	def stopwordRemoval(self, string):
		#stop words list
		# with open("anandhibot/stopwords.txt", "rb") as f:
		# 	for line in f:
		# 		stopwords = line.split(" ")
		# stopwords = set(open("%s/carolapp/stopwords.txt" % STATIC_ROOT).read().split(" "))
		stopwords = ["yang", "dengan", "itu", "ya", "di", "maksud", "ini", "dimaksud", "untuk", "pengertian", "bekerja", "ada", "berada", "belajar", "mempelajari", "saja", "pelajaran","sih"]

		checks = string.split(" ")
		output = ""

		for c in checks:
			if c not in stopwords:
				# c = unicodedata.normalize('NFKD', c).encode('ascii','ignore')
				c = re.sub('[!,?]', '', c)
				output = output + " " + c

		return output[1:]
