import time
import cv2
import mss
import numpy
import pytesseract


def bOrW(i):
    with mss.mss() as sct:
        box = {'top': 348+52*i, 'left': 1190, 'width': 80, 'height': 52}
        im=sct.grab(box)
        im = numpy.asarray(im)
        cv2.imwrite('num.png', im)
        scale=200
        im=cv2.resize(im,(int(im.shape[1] * scale / 100), int(im.shape[0] * scale / 100)))
        kernel = numpy.array([[0, -1, 0],
                    [-1, 5,-1],
                    [0, -1, 0]])
        im = cv2.filter2D(src=im, ddepth=-1, kernel=kernel)
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string(im,config=r'--oem 3 --psm 6').strip()
        print(text)

bOrW(1)