import PIL.Image
import ImageDraw
import ImageFont
import ImageFilter
import HTMLParser
import sys
import os

html_unescape_dict = {"a" : "yourmom", "&amp;" : "&", "&quot;" : "\"", "&apos;" : "'", "&gt;" : ">", "&lt;" : "<"}

f = open("/home/ubuntu/OCRplus/render_log.txt", "a")
f.write("yada\n")
f.close()

delimiter = "#OppanOCRplusDelimiter#"
remove_inner_newlines = 1
font_file_name = "/home/ubuntu/OCRplus/Rendering/coolvetica.ttf"
num_blurs = 50
min_font_size = 12
initial_font_size_blowup = 2.0
font_shrink = 0.9
max_bbox_coverage = 0.25

def text_fits(wmax, hmax, font_size, text):
	font = ImageFont.truetype(font_file_name, int(round(font_size)))
	(w, h) = font.getsize(text)
	return w < wmax and h < hmax

def draw_text_on_image(I, draw, x_offset, y_offset, lr_x_offset, lr_y_offset, font_size, red, green, blue, text):
	font_size *= initial_font_size_blowup
	while font_size > min_font_size and not text_fits(lr_x_offset - x_offset, lr_y_offset - y_offset, font_size, text):
		font_size *= font_shrink

	os.system("echo \"font_size = %f\" >> /home/ubuntu/OCRplus/Rendering/render_log.txt"%(font_size))

	draw.text((x_offset, y_offset), HTMLParser.HTMLParser().unescape(text), (red, green, blue), font = ImageFont.truetype(font_file_name, int(round(font_size))))

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
	input_strs[9 * i + 8].replace("&quot;", "\"")
	texts.append(input_strs[9 * i + 8])

I = PIL.Image.open(input_image_name)
draw = ImageDraw.Draw(I)
bgs = []
should_render = []
for i in range(len(texts)):
	bbox = (x_offsets[i], y_offsets[i], lr_x_offsets[i], lr_y_offsets[i])
	#patch = I.crop(bbox)
	p = I.load()
	ravg = 255
	gavg = 255
	bavg = 255
	#s = 1
	#for v in range(s):
	#	for h in range(s):
	#		(r, g, b) = p[x_offsets[i] + h, y_offsets[i] + v]
	#		ravg += r
	#		gavg += g
	#		bavg += b

	#ravg /= s ** 2
	#gavg /= s ** 2 
	#bavg /= s ** 2
	bgs.append((ravg, gavg, bavg))
	if (1.0 * (lr_x_offsets[i] - x_offsets[i]) * (lr_y_offsets[i] - y_offsets[i])) / (1.0 * I.size[0] * I.size[1]) <= max_bbox_coverage:
		draw.rectangle([(x_offsets[i], y_offsets[i]), (lr_x_offsets[i], lr_y_offsets[i])], fill = bgs[i])
		should_render.append(1)
	else:
		should_render.append(0)

	#for b in range(num_blurs):
	#

	#patch = patch.filter(ImageFilter.BLUR)

	#I.paste(patch, bbox)

#p = I.load()
for i in range(len(texts)):
	#(r, g, b) = p[(x_offsets[i] + lr_x_offsets[i]) / 2, (y_offsets[i] + lr_y_offsets[i]) / 2]
	(r, g, b) = bgs[i]
	if r < 128:
		r = 255
	else:
		r = 0

	if g < 128:
		g = 255
	else:
		g = 0

	if b < 128:
		b = 255
	else:
		b = 0

	if should_render[i]:
		draw_text_on_image(I, draw, x_offsets[i], y_offsets[i], lr_x_offsets[i], lr_y_offsets[i], font_sizes[i], r, g, b, texts[i])

I.save(output_image_name)

f = open("/home/ubuntu/OCRplus/render_log.txt", "a")
f.write("op op op\n")
f.close()
