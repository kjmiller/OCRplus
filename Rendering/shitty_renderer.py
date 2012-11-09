import PIL.Image
import ImageDraw
import ImageFont
import ImageFilter
import sys

delimiter = "#OppanOCRplusDelimiter#"
remove_inner_newlines = 1
font_file_name = "/home/ubuntu/OCRplus/Rendering/Lobster1.4.otf"
num_blurs = 25

def draw_text_on_image(I, draw, x_offset, y_offset, font_size, red, green, blue, text):
	draw.text((x_offset, y_offset), text, (red, green, blue), font = ImageFont.truetype(font_file_name, font_size))

input_image_name = sys.argv[1]
input_file_name = sys.argv[2]
output_image_name = sys.argv[3]

print(input_file_name)

input_file = open(input_file_name, "r")
input_str = ""
for line in input_file:
	if remove_inner_newlines:
		input_str += line.rstrip("\n")
	else:
		input_str += line

input_file.close()
input_str = input_str.rstrip("\n")
input_strs = input_str.split(delimiter)

x_offsets = []
y_offsets = []
lr_x_offsets = []
lr_y_offsets = []
font_sizes = []
reds = []
greens = []
blues = []
texts = []
for i in range(len(input_strs) / 9):
	x_offsets.append(int(input_strs[9 * i]))
	y_offsets.append(int(input_strs[9 * i + 1]))
	lr_x_offsets.append(int(input_strs[9 * i + 2]))
	lr_y_offsets.append(int(input_strs[9 * i + 3]))
	font_sizes.append(int(input_strs[9 * i + 4]))
	reds.append(int(input_strs[9 * i + 5]))
	greens.append(int(input_strs[9 * i + 6]))
	blues.append(int(input_strs[9 * i + 7]))
	texts.append(input_strs[9 * i + 8])

I = PIL.Image.open(input_image_name)
draw = ImageDraw.Draw(I)
for i in range(len(texts)):
	bbox = (x_offsets[i], y_offsets[i], lr_x_offsets[i], lr_y_offsets[i])
	patch = I.crop(bbox)
	for b in range(num_blurs):
		patch = patch.filter(ImageFilter.BLUR)

	I.paste(patch, bbox)

for i in range(len(texts)):
	draw_text_on_image(I, draw, x_offsets[i], y_offsets[i], font_sizes[i], reds[i], greens[i], blues[i], texts[i])

I.save(output_image_name)
