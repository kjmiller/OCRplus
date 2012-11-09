import os
import sys

intermediate_dir = "/home/ubuntu/OCRplus/intermediate"

def usage():
	print("Usage: python front_facing_backend.py <input_image_file_name> <source_language> <target_language> <output_image_file_name>")
	print("For list of acceptable source languages: see left column of /home/ubuntu/OCRplus/tesseract_language_dict.txt")
	print("For list of acceptable target languages: see left column of /home/ubunut/OCRplus/google_language_dict.txt")

def load_dict(dict_file_name):
	language_code_dict = {}
	dict_file = open(dict_file_name, "r")
	for line in dict_file:
		stuff = line.rstrip("\n").split(",")
		language_code_dict[stuff[0].lower()] = stuff[1]

	dict_file.close()
	return language_code_dict

if __name__ == "__main__":
	google_dict = load_dict("/home/ubuntu/OCRplus/google_language_dict.txt")
	tesseract_dict = load_dict("/home/ubuntu/OCRplus/tesseract_language_dict.txt") 
	input_image_file_name = sys.argv[1]
	source_language = sys.argv[2].lower()
	target_language = sys.argv[3].lower()
	output_image_file_name = sys.argv[4]

	tesseract_file_name = "%s/tesseracted"%(intermediate_dir)
	parse_file_name = "%s/parsed.txt"%(intermediate_dir)
	render_file_name = "%s/to_render.txt"%(intermediate_dir)

	os.system("rm %s %s %s"%(tesseract_file_name, parse_file_name, render_file_name))

	print("python /home/ubuntu/OCRplus/Backend/backend.py %s %s %s %s %s %s %s %s"%(input_image_file_name, tesseract_dict[source_language], google_dict[source_language], google_dict[target_language], tesseract_file_name, parse_file_name, render_file_name, output_image_file_name))
	os.system("python /home/ubuntu/OCRplus/Backend/backend.py %s %s %s %s %s %s %s %s"%(input_image_file_name, tesseract_dict[source_language], google_dict[source_language], google_dict[target_language], tesseract_file_name, parse_file_name, render_file_name, output_image_file_name))
