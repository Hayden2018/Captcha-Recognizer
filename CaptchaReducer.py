import numpy as np
from PIL import Image
import os


class CaptchaReducer:

    def __init__(self, bg):
        self.bg = np.array(Image.open(bg), dtype=np.int16)
        pass

    # Allow the instance of this class to be called like a function
    def __call__(self, filename):
        if isinstance(filename, np.ndarray):
            self.captcha = filename
            self.captcha = self.remove_line()
            self.captcha = self.remove_background()
            return self.captcha
        else:
            self.captcha = np.array(Image.open(filename), dtype=np.uint16)
            self.filename = filename
            self.captcha = self.remove_line()
            self.captcha = self.remove_background()
            self.captcha = Image.fromarray(self.captcha)
            self.captcha.save(self.filename)
            print('Saved as:', self.filename)

    # remove background color in captcha so that only words and a line is left.
    # if the difference of a pixel between 2 images is smaller than 10, then make it black.
    # The input should be two 3D np array and returning a 3D np array.
    def remove_background(self):
        BLACK = [0, 0, 0]
        WHITE = [255, 255, 255]
        color_difference_threshold = 10
        tmp = []
        captcha = self.captcha
        bg = self.bg

        # loop through every pixel in captcha and bg. If the color difference of RGB in two pictures is smaller than
        # the threshold, then it should be a part of background, and mark it as black. Else mark it as white.
        for j in range(50):
            tmp.append([])
            for captcha_pixel, bg_pixel in zip(captcha[j], bg[j]):
                if abs(captcha_pixel[0] - WHITE[0]) < color_difference_threshold and abs(
                        captcha_pixel[1] - WHITE[1]) < color_difference_threshold and abs(
                        captcha_pixel[2] - WHITE[2]) < color_difference_threshold or abs(captcha_pixel[0] - bg_pixel[0]) < color_difference_threshold and abs(
                        captcha_pixel[1] - bg_pixel[1]) < color_difference_threshold and abs(
                        captcha_pixel[2] - bg_pixel[2]) < color_difference_threshold:
                    tmp[j].append(BLACK)
                else:
                    tmp[j].append(WHITE)

        # Convert numpy array to image object
        captcha = Image.fromarray(np.uint8(tmp)).convert('L')
        captcha = np.array(captcha)
        return captcha

    # because when this function is called, the final result is not yet stored into self.captcha.
    # Therefore staticmethod is used here and just directly passing the temporary object.
    @staticmethod
    def pixel_aside_is_black(captcha, a, b, threshold):
        BLACK = [0, 0, 0]
        for j in range(-1+b, 2+b):
            for i in range(-1+a, 2+a):
                # Now fixed some small white pixel appearing on the top and bottom of the image.
                if i <= 0 or j <= 0 or (i == a and j == b) or i >= 199 or j >= 49:
                    continue
                if abs(int(captcha[j][i][0]) - int(BLACK[0])) < threshold and abs(int(captcha[j][i][1]) - int(BLACK[1])) < threshold and abs(int(captcha[j][i][2]) - int(BLACK[2])) < threshold:
                    return True
        return False

    # remove the line in RGB image.
    # Also if the pixel is beside or is extreme dark color, remove itself.
    def remove_line(self):
        captcha = self.captcha
        BLACK = [0, 0, 0]
        WHITE = [255, 255, 255]
        COLOR = BLACK
        threshold = 10
        tmp = captcha

        for j in range(50):
            for i, captcha_pixel in enumerate(captcha[j]):
                if self.pixel_aside_is_black(tmp, i, j, threshold) or abs(int(captcha_pixel[0]) - int(COLOR[0])) < threshold and abs(int(captcha_pixel[1]) - int(COLOR[1])) < threshold and abs(int(captcha_pixel[2]) - int(COLOR[2])) < threshold:
                    tmp[j][i] = WHITE.copy()

        captcha = np.array(tmp)
        return captcha


def main():
    cwd = os.getcwd()
    BACKGROUND = '/background.png'
    CAPTCHA_PATH = '/Original Data'

    reducer = CaptchaReducer(cwd + BACKGROUND)
    # Recursively reduce all bg in current directory

    for directories, folders, files in os.walk(cwd + CAPTCHA_PATH):
        os.chdir(directories)
        for file in files:
            if file.endswith('.png'):
                reducer(file)


if __name__ == "__main__":
    main()
