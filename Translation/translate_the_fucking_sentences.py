import urllib
import simplejson
import sys

base_url = "https://www.googleapis.com/language/translate/v2?"

sys_argv = " ".join(sys.argv[1:]).split("#")

key_file_name = sys_argv[0]
source = sys_argv[1]
target = sys_argv[2]
sentences = sys_argv[3:]

key_file = open(key_file_name, "r")
key = key_file.readline().rstrip("\n")
key_file.close()

source_tuple_list = []
if source != "":
	source_tuple_list = [("source", source)]

url = base_url + urllib.urlencode([("key", key)] + map(lambda sentence: ("q", sentence), sentences) + source_tuple_list + [("target", target)])

for blob in simplejson.load(urllib.urlopen(url))["data"]["translations"]:
	print(blob["translatedText"])
