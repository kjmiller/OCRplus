import os
import sys

delimiter = "#OppanOCRplusDelimiter#"
base_dir = "/home/ubuntu/OCRplus"
remove_inner_newlines = 1
font_coeff = 2.0

def usage():
	print("Usage: python backend.py <input_image_file_name> <tesseract_source_language> <google_source_language> <target_language> <tesseract_output_file_name> <parser_output_file_name> <rendering_input_file_name> <output_image_file_name>")

if __name__ == "__main__":
	log_file_name = base_dir + "/backend_log.txt"
	log_file = open(log_file_name, "a")
	log_file.write(" ".join(sys.argv) + "\n")
	
	input_image_file_name = sys.argv[1]
	tesseract_source_language = sys.argv[2]
	google_source_language = sys.argv[3]
	target_language = sys.argv[4]
	tesseract_output_file_name = sys.argv[5]
	parser_output_file_name = sys.argv[6]
	rendering_input_file_name = sys.argv[7]
	output_image_file_name = sys.argv[8]

	os.system("%s/OCRKevinTake3/run_tesseract.sh %s %s %s"%(base_dir, input_image_file_name, tesseract_output_file_name, tesseract_source_language))
	os.system("python %s/OCRKevinTake3/skeleton_parser.py %s %s"%(base_dir, tesseract_output_file_name + ".html", parser_output_file_name))
	
	parser_output_file = open(parser_output_file_name, "r")
	parser_output_str = ""
	for line in parser_output_file:
		print(line)
		if remove_inner_newlines:
			parser_output_str += line.rstrip("\n")
		else:
			parser_output_str += line

	parser_output_file.close()
	parser_output_str = parser_output_str.rstrip("\n")

	parser_outputs = parser_output_str.split(delimiter)

	if len(parser_outputs) == 0:
		os.system("cp %s %s"%(input_image_file_name, output_image_file_name))
		exit()

	#sentences_to_translate = []
	bbox_upper_left_xs = []
	bbox_upper_left_ys = []
	bbox_lower_right_xs = []
	bbox_lower_right_ys = []

	for i in range(len(parser_outputs) / 2):
		#sentences_to_translate.append(parser_outputs[2 * i + 1])
		bbox_coords = parser_outputs[2 * i].split(" ")
		bbox_upper_left_xs.append(int(bbox_coords[0]))
		bbox_upper_left_ys.append(int(bbox_coords[1]))
		bbox_lower_right_xs.append(int(bbox_coords[2]))
		bbox_lower_right_ys.append(int(bbox_coords[3]))

	translation_output = os.popen("python %s/Translation/translate_the_fucking_sentences.py %s/Translation/key.txt %s %s %s"%(base_dir, base_dir, google_source_language, target_language, parser_output_file_name))

	translation_output_str = ""
	for line in translation_output:
		if remove_inner_newlines:
			translation_output_str += line.rstrip("\n")
		else:
			translation_output_str += line

	translation_output_str = translation_output_str.rstrip("\n")
	log_file.write(translation_output_str + "\n")
	print(translation_output_str)
	log_file.write("STYLE\n")
	translated_sentences = translation_output_str.split(delimiter)

	if len(translated_sentences) == 0:
		log_file.write("shit\n")
		log_file.close()
		os.system("cp %s %s"%(input_image_file_name, output_image_file_name))
		exit()

	#log_file.close()

	rendering_input_strs = []
	for i in range(len(translated_sentences)):
		log_file.write(str(i) + "\n")
		rendering_input_strs.append(str(bbox_upper_left_xs[i]) + delimiter + str(bbox_upper_left_ys[i]) + delimiter + str(bbox_lower_right_xs[i]) + delimiter + str(bbox_lower_right_ys[i]) + delimiter + str(int(font_coeff * (bbox_lower_right_ys[i] - bbox_upper_left_ys[i]))) + delimiter + "0" + delimiter + "0" + delimiter + "0" + delimiter + translated_sentences[i])

	log_file.write("EHHH SEXY LADY\n")

	log_file.close()
	
	file_for_renderer = open(rendering_input_file_name, "w")
	file_for_renderer.write(delimiter.join(rendering_input_strs) + "\n")
	file_for_renderer.close()
	os.system("python %s/Rendering/shitty_renderer.py %s %s %s"%(base_dir, input_image_file_name, rendering_input_file_name, output_image_file_name))
	#log_file.write("YOU KNOW WHAT I'M SAYIN'\n")
	#log_file.close()
