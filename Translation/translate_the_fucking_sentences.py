import urllib
import simplejson
import sys

chunk_size = 1 #NOTE: DO NOT CHANGE THIS NUMBER!!!
remove_inner_newlines = 1

delimiter = "#OppanOCRplusDelimiter#"

base_url = "https://www.googleapis.com/language/translate/v2?"

key_file_name = sys.argv[1]
target = sys.argv[2]
input_file_name = sys.argv[3]

key_file = open(key_file_name, "r")
key = key_file.readline().rstrip("\n")
key_file.close()

parser_output_file = open(input_file_name, "r")
parser_output_str = ""
for line in parser_output_file:
	if remove_inner_newlines:
		parser_output_str += line.rstrip("\n")
	else:
		parser_output_str += line

parser_output_file.close()
parser_output_str = parser_output_str.rstrip("\n")

parser_outputs = parser_output_str.split(delimiter)

if len(parser_outputs) == 0:
	print("")
	exit()

sentences = []

for i in range(len(parser_outputs) / 2):
	sentences.append(parser_outputs[2 * i + 1].rstrip("\n"))

#print(sentences)

source_tuple_list = []
#if source != "":
#	source_tuple_list = [("source", source)]

translations = []
i = 0
while i * chunk_size < len(sentences):
	url = base_url + urllib.urlencode([("key", key)] + map(lambda sentence: ("q", sentence), sentences[i * chunk_size:min((i + 1) * chunk_size, len(sentences))]) + source_tuple_list + [("target", target)])

	#print(url)

	thingy = simplejson.load(urllib.urlopen(url))
	if "data" in thingy and  "translations" in thingy["data"]:
		for blob in thingy["data"]["translations"]:
			translations.append(blob["translatedText"])
	
	else:
		translations.append("")

	i += 1
	#print(translations)

print(delimiter.join(translations).encode('utf8'))
