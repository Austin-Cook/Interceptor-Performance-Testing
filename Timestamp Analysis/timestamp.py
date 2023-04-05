# Represents a Timestamp object

class Timestamp():
	def __init__(self, code, sec, usec):
		self.code = code
		self.sec = sec
		self.usec = usec
	
	def to_string(self):
		return self.code + " " + str(self.sec) + ":" + str(self.usec)
