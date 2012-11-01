from PIL.Image import open
import ImageDraw
import ImageFont
import sys

def font_file_name = "Lobster 1.4.otf"

def draw_text_on_image(I, draw, x_offset, y_offset, font_size, red, green, blue, text):
	draw.text((x_offset, y_offset), text, (red, green, blue), font = ImageFont.truetype(font_file_name, font_size))

sys_argv = " ".join(sys.argv[1:]).split("#")
input_image_name = sys_argv[0]
output_image_name = sys_argv[1]
for i in range((len(sys_argv) - 2) / 7):
	x_offsets.append(sys_argv[2 + 7 * i])
	y_offsets.append(sys_argv[2 + 7 * i + 1])
	font_sizes.append(sys_argv[2 + 7 * i + 2])
	reds.append(sys_argv[2 + 7 * i + 3])
	greens.append(sys_argv[2 + 7 * i + 4])
	blues.append(sys_argv[2 + 7 * i + 5])
	texts.append(sys_argv[2 + 7 * i + 6])

I = open(input_image_name)
draw = ImageDraw.Draw(I)
for i in range(len(texts)):
	draw_text_on_image(I, draw, x_offsets[i], y_offsets[i], font_sizes[i], reds[i], greens[i], blues[i], texts[i])

I.save(output_image_name)
