import os
import sys

delimiter = "#OppanOCRplusDelimiter#"
base_dir = "/afs/ir.stanford.edu/users/k/j/kjmiller/cgi-bin/OCRplus"
remove_inner_newlines = 1
font_coeff = 1.0

def usage():
	print("Usage: python backend.py <input_image_file_name> <target_language> <tesseract_output_file_name> <parser_output_file_name> <output_image_file_name>")

if __name__ == "__main__":
	input_image_file_name = sys.argv[1]
	target_language = sys.argv[2]
	tesseract_output_file_name = sys.argv[3]
	parser_output_file_name = sys.argv[4]
	output_image_file_name = sys.argv[5]

	os.system("%s/OCRKevinTake3/run_tesseract.sh %s %s"%(base_dir, input_image_file_name, tesseract_output_file_name))
	os.system("%s/OCRKevinTake3/src/parser %s %s"%(base_dir, tesseract_output_file_name + ".html", parser_output_file_name))
	
	parser_output_file = open(parser_output_file_name, "r")
	parser_output_str = ""
	for line in parser_output_file:
		if remove_inner_newlines:
			parser_output_str += line.rstrip("\n")
		else:
			parser_output_str += line

	parser_output_file.close()
	parser_output_str = parser_output_str.rstrip("\n")

	parser_outputs = parser_output_str.split(delimiter)[:-1]

	if len(parser_outputs) == 0:
		os.system("cp %s %s"%(input_image_file_name, output_image_file_name))
		exit()

	sentences_to_translate = []
	bbox_upper_left_xs = []
	bbox_upper_left_ys = []
	bbox_lower_right_xs = []
	bbox_lower_right_ys = []
	
	for i in range(len(parser_outputs) / 2):
		sentences_to_translate.append(parser_outputs[2 * i + 1])
		bbox_coords = parser_outputs[2 * i].split(" ")
		bbox_upper_left_xs.append(int(bbox_coords[0]))
		bbox_upper_left_ys.append(int(bbox_coords[1]))
		bbox_lower_right_xs.append(int(bbox_coords[2]))
		bbox_lower_right_ys.append(int(bbox_coords[3]))

	print("python %s/Translation/translate_the_fucking_sentences.py %s/Translation/key.txt%s%s%s%s%s"%(base_dir, base_dir, delimiter, delimiter, target_language, delimiter, delimiter.join(sentences_to_translate)))
	os.system("python %s/Translation/translate_the_fucking_sentences.py %s/Translation/key.txt%s%s%s%s%s"%(base_dir, base_dir, delimiter, delimiter, target_language, delimiter, delimiter.join(sentences_to_translate)))
	print("YAY")
	translation_output = os.popen("python %s/Translation/translate_the_fucking_sentences.py %s/Translation/key.txt%s%s%s%s%s"%(base_dir, base_dir, delimiter, delimiter, target_language, delimiter, delimiter.join(sentences_to_translate)))

	translation_output_str = ""
	for line in translation_output:
		if remove_inner_newlines:
			translation_output_str += line.rstrip("\n")
		else:
			translation_output_str += line

	translation_output_str = translation_output_str.rstrip("\n")
	print(translation_output_str)
	translated_sentences = translation_output_str.split(delimiter)

	if len(translated_sentences) == 0:
		os.system("cp %s %s"%(input_image_file_name, output_image_file_name))
		exit()

	rendering_input_strs = []
	for i in range(len(translated_sentences)):
		rendering_input_strs.append(str(bbox_upper_left_xs[i]) + delimiter + str(bbox_upper_left_ys[i]) + delimiter + str(int(font_coeff * (bbox_lower_right_ys[i] - bbox_upper_left_ys[i]))) + delimiter + "0" + delimiter + "0" + delimiter + "0" + delimiter + translated_sentences[i])

	os.system("python %s/Rendering/shitty_renderer.py "%(base_dir) + input_image_file_name + delimiter + output_image_file_name + delimiter + delimiter.join(rendering_input_strs))
