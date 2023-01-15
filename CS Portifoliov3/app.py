# Import the necessary libraries
from flask import Flask, render_template, request
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
import random

# Create a Flask app
app = Flask(__name__)

# Define the routes for the different pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/multi-functional-ai')
def ai_hand_control():
    return render_template('multi-functional-ai.html')

@app.route('/multi-functional-ai/demo')
def ai_hand_control_demo():
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector(detectionCon=0.7)
    lmList = []
    sw, sh = pyautogui.size()
    pyautogui.FAILSAFE = False
    mode = 0
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volRange =volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    running = True

    while running:
        success, img = cap.read()
        img = detector.findHands(img, draw=False)
        img = cv2.resize(img, None, None, fx=1.5, fy=1.5)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:

            x1, y1 = lmList[12][1], lmList[12][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            x3, y3 = lmList[5][1], lmList[5][2]
            x4, y4 = lmList[17][1], lmList[17][2]
            x5, y5 = lmList[4][1], lmList[4][2]
            x6, y6 = lmList[16][1], lmList[16][2]

            length1 = math.hypot((x2 - x1), (y2 - y1))
            length2 = math.hypot((x5-x2), (y5-y2))
            length3 = math.hypot((x5-x1),(y5-y1))
            length4 = math.hypot((x6-x5), (y6-y5))

            hmax = math.hypot((x4 - x3), (y4 - y3))

            if length3< hmax*.4:
                mode = 0
            if length4<hmax*.4:
                mode = 1
            if sum(detector.findFingersUp(img)) == 0:
                mode = 2

            if mode == 0:
                cv2.putText(img, 'AI Mouse Control', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (117, 116, 42), 3)
                cv2.rectangle(img, (120,520), (550,90), (255,0,255), 2)

                if length1<hmax:
                    cv2.circle(img, (x2, y2), 10, (0, 0, 225), cv2.FILLED)
                elif length2<hmax*0.4:
                    pyautogui.click()
                    cv2.circle(img, (x5, y5), 5, (255 , 0, 0), cv2.FILLED)
                else:
                    cv2.circle(img, (x2, y2), 10, (225, 0, 225), cv2.FILLED)
                    h, w, c = img.shape
                    x6 = np.interp(x2, (120, 550), (0, sw))
                    y6 = np.interp(y2, (90, 520), (0, sh))

                    pyautogui.moveTo(sw-x6, y6)
            if mode == 1:
                cv2.putText(img, 'AI Volume Control', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (117, 116, 42), 3)
                hmax *= 2
                cx1, cy1 = int((x2 + x5) / 2), int((y2 + y5) / 2)
                cx2, cy2 = int((x1 + x2) / 2), int((y1 + y2) / 2)

                cv2.circle(img, (x5, y5), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x5, y5), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx1, cy1), 5, (255, 0, 255), cv2.FILLED)

                vol = np.interp(length2, [20, hmax], [minVol, maxVol])
                volBar = np.interp(length2, [20, hmax], [400, 150])
                volPer = np.interp(length2, [20, hmax], [0, 1]) * 100

                if length1 < hmax * 0.5:
                    cv2.circle(img, (cx2, cy2), 5, (255, 0, 0), cv2.FILLED)
                else:
                    volume.SetMasterVolumeLevel(vol, None)
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f': {int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
            if mode == 2:
                cv2.putText(img, 'AI Keyboard Shortcut Control', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (117, 116, 42), 3)
                if detector.findFingersUp(img) == [1,0,0,0,0]:
                    pyautogui.hotkey('alt', 'tab')
                    cv2.putText(img, 'Alt + Tab', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                    time.sleep(1)

                if detector.findFingersUp(img) == [0,1,0,0,0]:
                    pyautogui.hotkey('win', 'tab')
                    cv2.putText(img, 'Win + Tab', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                    time.sleep(1)

                if detector.findFingersUp(img) == [0,1,1,0,0]:
                    pyautogui.hotkey('win', 'prtsc')
                    cv2.putText(img, 'Win + Prtsc', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                    time.sleep(1)

                if detector.findFingersUp(img) == [0,0,1,1,1]:
                    pyautogui.hotkey('win', 'd')
                    cv2.putText(img, 'Win + D', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                    time.sleep(1)
        else:
            cv2.putText(img, 'No hands detected', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (117, 116, 42), 3)
        
        cv2.imshow("Image", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            running = False
    cap.release()
    cv2.destroyAllWindows()
    return render_template('multi-functional-ai.html')

@app.route('/gsg')
def gsg():
    return render_template('gsg.html')

@app.route('/gsg/demo')
def gsg_demo():

    # Initialize pygame
    pygame.init()

    # Set the window size and title
    WINDOW_SIZE = (300, 300)
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Color Swap Game')

    # Set the colors
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    # Set the number of rows and columns
    ROWS = 3
    COLUMNS = 3

    # Set the size of each tile
    TILE_SIZE = 100

    # Set the margin between tiles
    MARGIN = 10

    # Create a 2D list to store the colors of each tile
    tiles = [[random.choice([BLUE, GREEN]) for _ in range(COLUMNS)] for _ in range(ROWS)]

    # Set the font for the victory screen
    font = pygame.font.Font(None, 36)

    # Set the game state
    game_over = False

    # Main game loop
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                pos = pygame.mouse.get_pos()
                # Convert the mouse position to a grid index
                column = pos[0] // (TILE_SIZE + MARGIN)
                row = pos[1] // (TILE_SIZE + MARGIN)
                # Swap the color of the clicked tile and its adjacent tiles
                tiles[row][column] = GREEN if tiles[row][column] == BLUE else BLUE
                if row > 0:
                    tiles[row - 1][column] = GREEN if tiles[row - 1][column] == BLUE else BLUE
                if row < ROWS - 1:
                    tiles[row + 1][column] = GREEN if tiles[row + 1][column] == BLUE else BLUE
                if column > 0:
                    tiles[row][column - 1] = GREEN if tiles[row][column - 1] == BLUE else BLUE
                if column < COLUMNS - 1:
                    tiles[row][column + 1] = GREEN if tiles[row][column + 1] == BLUE else BLUE

        # Draw the tiles
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = tiles[row][column]
                pygame.draw.rect(window, color, [
                    (MARGIN + TILE_SIZE) * column + MARGIN,
                    (MARGIN + TILE_SIZE) * row + MARGIN,
                    TILE_SIZE,
                    TILE_SIZE
                ])

        # Check if the game is won
        if all(color == GREEN for row in tiles for color in row):
            # Display the victory screen
            text = font.render('You won!', True, GREEN)
            text_rect = text.get_rect()
            text_rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]// 2)
            window.blit(text, text_rect)
            pygame.display.flip()
            game_over = True

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    
    return render_template('gsg.html')

@app.route('/pnp')
def pnp():
    return render_template('pnp.html')

@app.route('/blt')
def blt():
    return render_template('blt.html')

@app.route('/rc')
def rc():
    return render_template('rc.html')


# Run the app
if __name__ == '__main__':
    app.run()
