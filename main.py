# Made by: ElReyZero
#Script to identify the occurence of a death while you're XP AFK farming

import cv2
import pyautogui
import numpy as np
import time
from datetime import datetime
from pynput.keyboard import Key, Controller
import os
import msvcrt

def writeDeathEvent():
    #Opening and writing time at which death occurred
    f = open("./logs/deathat.txt", "w+")
    f.write("Death occurred at: {0}".format(datetime.now()))
    f.close()
    #Stopping the macro
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    time.sleep(0.6)
    keyboard.press(Key.shift)
    time.sleep(0.6)
    keyboard.press(Key.alt)
    time.sleep(0.6)
    keyboard.press("p")
    time.sleep(0.6)
    keyboard.release("p")
    time.sleep(0.6)
    #Releasing keys
    keyboard.release(Key.ctrl)
    time.sleep(0.6)
    keyboard.release(Key.shift)
    time.sleep(0.6)
    keyboard.release(Key.alt)

    #Closing Destiny 2 (Alt+F4)
    time.sleep(5)
    keyboard.press(Key.alt)
    time.sleep(0.6)
    keyboard.press(Key.f4)
    keyboard.release(Key.alt)
    keyboard.release(Key.f4)
    #Shutting Down PC
    #time.sleep(10)
    #os.system("shutdown /s /t 1")


def chooseLanguage()->int:

    #Endless loop until the user exits the program or chooses a language
    choice = ""
    answered = False
    while not answered:
        choice = input("Choose your language:\n1. Spanish\n2. English\n3.Exit\n")
        try:
            if int(choice) == 1:
                print("Iniciando programa...")
                answered = True
                return 1
            elif int(choice) == 2:
                print("Starting program...")
                answered = True
                return 0
            elif int(choice) == 3:
                os.exit(1)
            else:
                print(choice + " is not a valid input.")
        except:
            print(choice + " is not a valid input.")

def main():

    #Language Selection
    lang = chooseLanguage()

    #Reading the screenshot of Light Fades Away according to the language
    if lang == 1:
        lightfades = cv2.imread("./img/luz.png")
    else:
        lightfades = cv2.imread("./img/light.png")

    method = cv2.TM_CCOEFF_NORMED

    #Read the images
    screenshot = None
    death_symbol = cv2.imread("./img/deathsymb.png")
    running = True
    death_symbol = cv2.cvtColor(death_symbol, cv2.COLOR_RGB2BGR)

    while running:
        # Take screenshot
        image = pyautogui.screenshot()

        # convert it to numpy array and BGR, to then write it on disk
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # writing it to the disk using opencv
        cv2.imwrite("./img/screenshot.png", image)

        # reading the screenshot
        screenshot = cv2.imread("./img/screenshot.png")


        #checking if the screenshot contains the death symbol
        result = cv2.matchTemplate(death_symbol, screenshot, method)

        if np.any(result>0.99):
            print("DeathSymbol was found in screenshot")
            #Calls death event function
            writeDeathEvent()
            #Stopping the program
            running = False
        else:
            #If deathsymbol is not found, we'll try to find the text "Your Light Fades Away"
            result = cv2.matchTemplate(lightfades, screenshot, method)
            if np.any(result>0.99):
                print("Lightfades was found in screenshot")
                #Calls death event function
                writeDeathEvent()
                #Stopping the program
                running = False
            else:
                print("Neither DeathSymbol nor Lightfades were found in screenshot")
        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == 27:
                break
        time.sleep(7)

main()


