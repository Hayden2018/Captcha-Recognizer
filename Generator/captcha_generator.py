# This program is for generating captcha. Captcha will be saved at /data/captcha.

from PIL import Image, ImageDraw, ImageFont
from random import randint, choice
import os


class Line:
    # Initializer parameters here
    def __init__(self, image):
        self.vflip = randint(0, 1)
        self.hflip = randint(0, 1)
        self.image = image
        # ratio
        # x, y pos (use Box parameter in Image.paste)

    # Augmentation will effect here
    def draw(self, image):
        if self.vflip:
            self.image.transpose(Image.FLIP_TOP_BOTTOM)
        if self.hflip:
            self.image.transpose(Image.FLIP_LEFT_RIGHT)
        # paste self.image to image.
        # image.paste(self.image, (0, 0), self.image)
        return Image.alpha_composite(image, self.image)


class CaptchaText:
    # Input a list with len = 5, eg ['a', 'b', '3', 'd', '5'] and font to be used
    def __init__(self, text, font, colour):
        self.text = text
        self.font = font
        self.colour = colour
        # self.image stores the captcha words generated.
        self.image = Image.new('RGBA', (200, 50), (0, 0, 0, 0))

    def draw(self, image):
        # Create a canvas.
        drawCanvas = ImageDraw.Draw(self.image)

        x = 11
        y = 5 - self.font.getoffset(self.text)[1]

        # By re-drawing the same pattern with offset +- 1 on each side, the stroke / outline of words can be formed.
        drawCanvas.text([x - 1, y - 1], self.text, fill=self.colour, font=self.font)
        drawCanvas.text([x + 1, y - 1], self.text, fill=self.colour, font=self.font)
        drawCanvas.text([x - 1, y + 1], self.text, fill=self.colour, font=self.font)
        drawCanvas.text([x + 1, y + 1], self.text, fill=self.colour, font=self.font)

        # Hollow the words by making it transparent.
        self.colour = (0, 0, 0, 0)
        drawCanvas.text([x, y], self.text, fill=self.colour, font=self.font)

        # image.paste(self.image, (0, 0), self.image)
        return Image.alpha_composite(image, self.image)


# n is the number of captcha to be generated
def captcha_generator(n):
    cwd = os.getcwd()
    FONT_PATH = '\data\\fonts\\'
    [FONTS] = [[file for file in files if file.endswith('.ttf') or file.endswith('.TTF')] for
               directories, folders, files in os.walk(cwd + FONT_PATH)]
    LINE_PATH = '\data\\line\\'
    [LINES] = [[file for file in files if file.endswith('.png')] for directories, folders, files in
               os.walk(cwd + LINE_PATH)]
    BACKGROUND_PATH = '\data\\'
    BACKGROUND = 'background.png'
    SAVE_PATH = '\data\\captcha\\'
    WORD_LIST = '23456789abcdefghkmnprwxy'

    BLUE = (130, 130, 255, 191)
    BLACK = (20, 20, 20, 170)

    # Create a new image by coping the background.
    background_layer = Image.open(os.path.join(os.getcwd() + BACKGROUND_PATH, BACKGROUND)).convert('RGBA')
    # background is now ready.

    for i in range(n):

        # Known problem:
        # image.paste(image2, (0, 0), image2) is malfunctioning when 'image' and 'image2' are 'RGBA'.
        # See:
        # https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
        # Solution: use 'Image.alpha_composite' instead.

        captcha = Image.new('RGBA', (200, 50))
        # captcha.paste(background_layer, (0, 0), background_layer)
        captcha = Image.alpha_composite(captcha, background_layer)

        # Generate a 5-digit word, from word list, repeatable.
        text = ''
        for a in range(5):
            text += choice(WORD_LIST)

        # Randomly select a type of fonts for generating captcha.
        font = choice(FONTS)

        # Randomly select colour of words, either blue or black.
        colour = choice([BLUE, BLACK])

        # draw them out by calling captcha text class.
        font_size = 45
        font_file = ImageFont.truetype(cwd + FONT_PATH + font, font_size)
        text_layer = CaptchaText(text, font_file, colour)
        captcha = text_layer.draw(captcha)

        # Randomly select a line type.
        line = choice(LINES)

        # add line on top of it
        # line_file = Image.open(cwd + LINE_PATH + line, "RGBA")
        line_file = Image.open(cwd + LINE_PATH + line)
        line_file = line_file.convert('RGBA')
        line_layer = Line(line_file)
        captcha = line_layer.draw(captcha)

        # save with the corresponding answer.
        captcha.save(cwd + SAVE_PATH + text + '.png', 'PNG')
        print('Saved as:', cwd + SAVE_PATH + text + '.png')


def main():
    captcha_generator(45000)


if __name__ == "__main__":
    main()
