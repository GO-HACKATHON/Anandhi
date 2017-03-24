class ClueWords:
	def __init__(self):
		self.clue = ""
		self.afterKeywords = []


	def __init__(self, clueword):
		self.clue = clueword
		self.setAfterKeywords(clueword)


	def setAfterKeywords(self, clueword):
		self.afterKeywords = []

		if clueword == "definisi":
			self.afterKeywords = ["adalah", "yaitu", "ialah", "merupakan", "diartikan"]
		elif clueword == "lokasi":
			self.afterKeywords = ["berada","bertempat","adanya","ada","tempat","tempatnya","berlokasi","terletak"]
		elif clueword == "prospek":
			self.afterKeywords = ["adalah", "yaitu", "ialah", "merupakan", "bekerja di","bekerja sebagai"]