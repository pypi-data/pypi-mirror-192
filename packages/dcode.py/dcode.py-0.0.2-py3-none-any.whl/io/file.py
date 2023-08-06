def read(file):
	try:
		with open(file, "rt") as file:
			return file.read()
	except e:
		return e

def write(file, content):
	try:
		with open(file, "wt") as file:
			return file.write(content)
	except e:
		return e
