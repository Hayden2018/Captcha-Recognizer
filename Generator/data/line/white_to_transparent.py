from PIL import Image
import os


def white_to_transparent(image):
    # Must be a tupe not a list
    transparency = (255, 255, 255, 0)
    # Convert to png format with alpha which represents transparency
    img = image.getdata()
    tmp = []
    for pixel in img:
        # if all the three channels RGB == 255:
        if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
            tmp.append(transparency)
        else:
            tmp.append(pixel)
    return tmp


def main():
    cwd = os.getcwd()
    for directories, folders, files in os.walk(cwd):
        for file in files:
            # if the file has .png
            if file.find('.png') != -1:
                image = Image.open(file)
                image = image.convert("RGBA")
                image.putdata(white_to_transparent(image))

                image.save(file, 'PNG')
                print('Saved as:', file)


if __name__ == "__main__":
    main()
