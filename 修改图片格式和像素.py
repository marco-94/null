from PIL import Image
for i in range(0, 34):
    image = Image.open("C:/Users/24540/Desktop/file/picture/" + str(i) + ".jpg")
    width = 1080
    height = 1080
    file_out = "C:/Users/24540/Desktop/file/picture/" + str(i) + ".jpg"
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)
