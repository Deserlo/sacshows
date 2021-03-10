from PIL import Image, ImageFont, ImageDraw 

my_image = Image.open("flyer_background.png")

title_font = ImageFont.truetype('RocknRollOne-Regular.ttf', 70)

title_text = "TONIGHT'S SHOWS"

image_editable = ImageDraw.Draw(my_image)

image_editable.rectangle((20, 30, 760, 140), outline='black', fill='black')
image_editable.text((39,28), title_text, (255, 255, 255), font=title_font, stroke_width=3)

list_font = ImageFont.truetype('RocknRollOne-Regular.ttf', 30)
image_editable.rectangle((300, 240, 560, 140), outline='black', fill='black')
image_editable.text((220,138), "5p The Ramones@Torch Club", (255, 255, 255), font=list_font)

my_image.save("show_flyer_tonight.png")
