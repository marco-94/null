from PIL import Image
for i in range(0, 79):
	image = Image.open("D:/picccc/" + str(i) + ".jpg")
	width = 1920
	height = 1080
	file_out = "D:/picccc/" + str(i) + ".jpg"
	resized_image = image.resize((width, height), Image.ANTIALIAS)
	resized_image.save(file_out)
