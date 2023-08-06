def read(file):
	try:
		with open(file, "rt") as file:
			return file.read()
	except e:
		return e
