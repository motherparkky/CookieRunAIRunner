import pyautogui
import time
import cv2
import numpy as np
import random
import tkinter as tk
from threading import Thread, Lock
import pygetwindow as gw
import winsound

# Get the region of the specific window
def get_window_region(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        return (window[0].left, window[0].top, window[0].width, window[0].height)
    return None

# Image detection within a specific region
def locate_image(image_path, region=None, confidence=0.8):
    try:
        location = pyautogui.locateCenterOnScreen(image_path, region=region, confidence=confidence)
        if location:
            print(f"Image '{image_path}' found at {location}")
        else:
            print(f"Image '{image_path}' not found with confidence {confidence}")
        return location
    except Exception as e:
        print(f"Error locating image {image_path}: {e}")
        return None

# Clicking at a specific screen position
def click_position(position):
    if position is not None:
        pyautogui.click(position)

# Playing alert for card game
def play_alarm():
    try:
        winsound.MessageBeep(winsound.MB_ICONHAND)
    except Exception as e:
        print(f"Error playing system sound: {e}")

# Main game loop function
def game_loop(window_title):
    global running, last_screen, last_move_time, lock
    region = get_window_region(window_title)
    if not region:
        print(f"Window '{window_title}' not found.")
        return

    while True:
        with lock:
            if not running:
                break

        screen = pyautogui.screenshot(region=region)
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

        end_game_pos = locate_image('end_game.png', region=region, confidence=0.8)
        if end_game_pos:
            check_pos = locate_image('check_button.png', region=region, confidence=0.8)
            click_position(check_pos)
            time.sleep(1)

        mystery_gacha = locate_image('mystery_gacha.png', region=region, confidence=0.8)
        if mystery_gacha:
            mystery_pos = locate_image('mystery_button.png', region=region, confidence=0.8)
            click_position(mystery_pos)
            time.sleep(3)
            click_position(mystery_pos)
            time.sleep(3)

        start_game_pos = locate_image('start_game.png', region=region, confidence=0.8)
        if start_game_pos:
            start_pos = locate_image('start_button.png', region=region, confidence=0.8)
            click_position(start_pos)
            time.sleep(1)

            #Automatic boost purchase Algorithm
            boost_pos = locate_image('boost_button_1200.png', region=region, confidence=0.8)
            click_position(boost_pos)

            time.sleep(1)
            
            purchase_pos = locate_image('purchase_button.png', region=region, confidence=0.8)

            click_position(purchase_pos)

            time.sleep(2)

            coin_option = locate_image('coin_twice.png', region=region, confidence=0.8)

            while (1):
                if coin_option:
                    break
                click_position(purchase_pos)
                time.sleep(0.5)
                boost_purchase_pos = locate_image('boost_purchase.png', region = region, confidence=0.8)
                click_position(boost_purchase_pos)
                time.sleep(2)
                coin_option = locate_image('coin_twice.png', region=region, confidence=0.8)

            #Secondary runner purchase Algorithm
            second_pos = locate_image('second_button.png', region=region, confidence=0.8)
            click_position(second_pos)
            click_position(purchase_pos)
            time.sleep(1)

            click_position(start_pos)
            time.sleep(1)

        second_button_pos = locate_image('second_button_in_game.png', region=region, confidence=0.8)
        if second_button_pos:
            click_position(second_button_pos) #in game secondary button
            #need to figure out how to stop the game

        card_game_pos = locate_image('card_game.png', region=region, confidence=0.8)
        if card_game_pos:
            play_alarm()
        
            
        #To add more func, use this line-----

        time.sleep(1)

def start_macro():
    global running, lock
    with lock:
        running = True
    window_title = window_entry.get()
    thread = Thread(target=game_loop, args=(window_title,))
    thread.start()

def stop_macro():
    global running, lock
    with lock:
        running = False

# GUI setup
root = tk.Tk()
root.title("Game Automation")

tk.Label(root, text="Window Title:").pack()
window_entry = tk.Entry(root)
window_entry.pack()

start_button = tk.Button(root, text="Start", command=start_macro)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_macro)
stop_button.pack()

running = False
lock = Lock()
last_screen = None
last_move_time = time.time()

root.mainloop()
