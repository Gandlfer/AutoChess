
import time

import cv2
import mss
import numpy
import pytesseract
import chess
import chess.engine

sct=mss.mss()
top=258
countBreak=6
custom_config = r'--oem 3 --psm 12'
number_box={'top': top, 'left': 1000, 'width': 30, 'height': 52}
black = {'top': top, 'left': 1190, 'width': 80, 'height': 52}
white ={'top': top, 'left': 1050, 'width': 80, 'height': 52}
# black = {'top': 346, 'left': 1190, 'width': 80, 'height': 52}
# white ={'top': 346, 'left': 1050, 'width': 80, 'height': 52}
engine = chess.engine.SimpleEngine.popen_uci("D:\Projects\Python\AutoChess\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
board=chess.Board()

player=None
count=0
def getNumber(box):
    with mss.mss() as sct:
        while True:
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
            text = pytesseract.image_to_string(im,config=r'--oem 3 --psm 6').strip().replace(".","").replace(" ","")
            if(text!=""):
                return int(text)

def movedPiece(box):
    with mss.mss() as sct:
        print("Finding")
        while True:
            im=sct.grab(box)
            im = numpy.asarray(im)
            scale=200
            im=cv2.resize(im,(int(im.shape[1] * scale / 100), int(im.shape[0] * scale / 100)))
            cv2.imwrite('thres.png', im)
            kernel = numpy.array([[0, -1, 0],[-1, 5,-1],[0, -1, 0]])
            im = cv2.filter2D(src=im, ddepth=-1, kernel=kernel)
            pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            text = pytesseract.image_to_string(im,config=custom_config).strip().replace("0","O").replace(".","").replace(" ","")
            if text!="":
                break
                
    if("é" in text):
        if "6" in text:
            text=text.replace("é" ,"")
        else:
            text=text.replace("é" ,"6")
    print("Found {}".format(text))
    return text

def bOrW():
    box = {'top': 892, 'left': 911, 'width': 18, 'height': 18}
    im=sct.grab(box)
    im = numpy.asarray(im)
    cv2.imwrite('thresh.png', im)
    scale=200
    im=cv2.resize(im,(int(im.shape[1] * scale / 100), int(im.shape[0] * scale / 100)))
    kernel = numpy.array([[0, -1, 0],
                [-1, 5,-1],
                [0, -1, 0]])
    im = cv2.filter2D(src=im, ddepth=-1, kernel=kernel)
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(im,config=r'--oem 3 --psm 6').strip()
    if text=="a":
        return "black"
    else:
        return "white"

with mss.mss() as sct:
    player=bOrW()
    print("Player as {}".format(player))
    if player=="white":
        result = engine.play(board, chess.engine.Limit(time=0.1))
        print(result.move)
        board.push(result.move)
        count=0

        while True:
            if(player=="white" and board.turn):
                print("Move {}".format(count+1))
                result = engine.play(board, chess.engine.Limit(time=0.1))
                print(result.move)
                board.push(result.move)

            else:
                text= movedPiece(white if board.turn else black)
                num=getNumber(number_box)
                print(num)
                if num>count:
                    count=num
                    print(text)
                    board.push_san(text)
                    if count<countBreak:
                        number_box = {'top': top+52*count, 'left': 1000, 'width': 30, 'height': 52}
                        white ={'top': top+52*count, 'left': 1050, 'width': 80, 'height': 52}
                        black={'top': top+52*count, 'left': 1190, 'width': 80, 'height': 52}
                    else:
                        number_box = {'top': 540, 'left': 1000, 'width': 30, 'height': 52}
                        white ={'top': 540, 'left': 1050, 'width': 80, 'height': 52}
                        black={'top': 540, 'left': 1190, 'width': 80, 'height': 52}
            #time.sleep(2)
    # while True:
    #     if(player=="black" and not board.turn) or (player=="white" and board.turn):
    # if player=="white":
    #     while True:
    #         print("White" if board.turn else "Black")
    #         if(player=="black" and not board.turn) or (player=="white" and board.turn):
    #             result = engine.play(board, chess.engine.Limit(time=0.1))
    #             if player=="black":
    #                 blackMove=result.move
    #             if player=="white":
    #                 whiteMove=result.move
    #             if(not board.turn):
    #                 if count<5:
    #                     count=count+1
    #                     box = {'top': top+52*count, 'left': 1000, 'width': 30, 'height': 52}
    #                     white ={'top': top+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                     black={'top': top+52*count, 'left': 1190, 'width': 80, 'height': 52}
    #                     # white ={'top': 346+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                     # black={'top': 346+52*count, 'left': 1190, 'width': 80, 'height': 52}    
    #                 else:
    #                     box = {'top': 540, 'left': 1000, 'width': 30, 'height': 52}
    #                     white ={'top': 540, 'left': 1050, 'width': 80, 'height': 52}
    #                     black={'top': 540, 'left': 1190, 'width': 80, 'height': 52}
    #             print(result.move)
    #             board.push(result.move)

    #         else:
    #             #while True:
    #             text= movedPiece(white if board.turn else black)
    #                 # if board.turn and count>0:
    #                 #     if whiteMove!=text:
    #                 #         break
    #                 # elif not board.turn and count>0:
    #                 #     if blackMove!=text:
    #                 #         break
    #                 # else:
    #                 #     break
                    
    #             if(not board.turn):
    #                 if count<5:
    #                     count=count+1
    #                     box = {'top': top+52*count, 'left': 1000, 'width': 30, 'height': 52}
    #                     white ={'top': top+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                     black={'top': top+52*count, 'left': 1190, 'width': 80, 'height': 52}
    #                     # white ={'top': 346+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                     # black={'top': 346+52*count, 'left': 1190, 'width': 80, 'height': 52}    
    #                 else:
    #                     box = {'top': 540, 'left': 1000, 'width': 30, 'height': 52}
    #                     white ={'top': 540, 'left': 1050, 'width': 80, 'height': 52}
    #                     black={'top': 540, 'left': 1190, 'width': 80, 'height': 52}

    #             print("Moved")
    #             # if player=="black":
    #             #     whiteMove=text
    #             # elif player=="white":
    #             #     blackMove=text
    #             print(text)
    #             board.push_san(text)
    # elif player=="black":
    #     getNumber(number_box)
    #     if(player=="black" and not board.turn) or (player=="white" and board.turn):
    #             result = engine.play(board, chess.engine.Limit(time=0.1))
    #             if player=="black":
    #                 blackMove=result.move
    #             if player=="white":
    #                 whiteMove=result.move
    #             if(not board.turn):
    #                 if count<5:
    #                     count=count+1
    #                     box = {'top': top+52*count, 'left': 1000, 'width': 30, 'height': 52}
    #                     white ={'top': top+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                     black={'top': top+52*count, 'left': 1190, 'width': 80, 'height': 52}
    #                     # white ={'top': 346+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                     # black={'top': 346+52*count, 'left': 1190, 'width': 80, 'height': 52}    
    #                 else:
    #                     box = {'top': 540, 'left': 1000, 'width': 30, 'height': 52}
    #                     white ={'top': 540, 'left': 1050, 'width': 80, 'height': 52}
    #                     black={'top': 540, 'left': 1190, 'width': 80, 'height': 52}
    #             print(result.move)
    #             board.push(result.move)

    #     else:
    #         #while True:
    #         text= movedPiece(white if board.turn else black)
    #             # if board.turn and count>0:
    #             #     if whiteMove!=text:
    #             #         break
    #             # elif not board.turn and count>0:
    #             #     if blackMove!=text:
    #             #         break
    #             # else:
    #              #     break
                    
    #         if(not board.turn):
    #             if count<5:
    #                 count=count+1
    #                 box = {'top': top+52*count, 'left': 1000, 'width': 30, 'height': 52}
    #                 white ={'top': top+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                 black={'top': top+52*count, 'left': 1190, 'width': 80, 'height': 52}
    #                 # white ={'top': 346+52*count, 'left': 1050, 'width': 80, 'height': 52}
    #                 # black={'top': 346+52*count, 'left': 1190, 'width': 80, 'height': 52}    
    #             else:
    #                 box = {'top': 540, 'left': 1000, 'width': 30, 'height': 52}
    #                 white ={'top': 540, 'left': 1050, 'width': 80, 'height': 52}
    #                 black={'top': 540, 'left': 1190, 'width': 80, 'height': 52}

    #         print("Moved")
    #             # if player=="black":
    #             #     whiteMove=text
    #             # elif player=="white":
    #             #     blackMove=text
    #         print(text)
    #         board.push_san(text)