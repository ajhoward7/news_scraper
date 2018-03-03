import json

with open('output.json') as f:
	output = json.loads(f.read())

for key in output:
	print "------------\n"
	print "SOURCE: {}\n".format(key)
	print "------------"
	for value in output[key]:
		for sub_key in value:
			print u"{}: {}".format(sub_key, value[sub_key]).encode('utf8','ignore')
		print "\n"



