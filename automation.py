import keyboard
import mss
import os
import pyautogui
import time

from PIL import Image

TOGGLE_KEY = "num multiply"

pyautogui.PAUSE = 1/60

def check_killswitch():
    if (keyboard.is_pressed(TOGGLE_KEY)):
        quit(1)

def press(key):
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

def screenshot(name):
    with mss.mss() as ss:
        ss_img = ss.grab(ss.monitors[1])
        img = Image.frombytes("RGB", ss_img.size, ss_img.bgra, "raw", "BGRX")

        out = f"./bnuy_frames/{name}.png"
        img.save(out)

def cursor_move(ox, oy, dx, dy):
    while (ox != dx):
        check_killswitch()
        if (ox < dx):
            press("right")
            ox += 1
        elif (ox > dx):
            press("left")
            ox -= 1

    while (oy != dy):
        check_killswitch()
        if (oy < dy):
            press("down")
            oy += 1
        elif (oy > dy):
            press("up")
            oy -= 1

if __name__ == "__main__":
    keyboard.wait(TOGGLE_KEY)

    start_time = time.time()

    DIR = "./frame_data"
    file_count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    i = 940
    w = 40
    h = 20
    color_state = 0 # [0, 1]
    cursor_x = 0
    cursor_y = 0
    read_cursor_x = 0
    read_cursor_y = 0

    current_canvas = bytearray([0] * (w * h))
    diff_coords = []
    new_colors = []
    prev_color = 0

    while i < 3286:
        print(f"Frame {i}")

        diff_coords = []
        new_colors = []

        name = f"{(i + 1):04}"
        filename = os.path.join(DIR, name)

        with open(filename, "rb") as f:
            ba = bytearray(f.read())
            
            for cx in range(8):
                for cy in range(4):
                    for x in range(5):
                        for y in range(5):
                            rx = (5 * cx) + x
                            ry = (5 * cy) + y
                            index = ry * w + rx

                            if (current_canvas[index] != ba[index]):
                                diff_coords.append((rx, ry))
                                new_colors.append(ba[index])
            
            current_canvas = ba.copy()
        

        if (len(diff_coords) == 0):
            wait_loop = 240
            while (wait_loop < 0):
                check_killswitch()
                press("0")
                wait_loop -= 1
        else:
            new_colors_index = 0
            for (x, y) in diff_coords:
                check_killswitch()

                new_color = new_colors[new_colors_index]

                if (new_color == 255 and prev_color == 0):
                    press("1")
                if (new_color == 0 and prev_color == 255):
                    press("3")
                
                prev_color = new_color
                    
                cursor_move(cursor_x, cursor_y, x, y)
                cursor_x = x
                cursor_y = y

                press("space")

                new_colors_index += 1
            
        screenshot(name)

        i += 1
    
    print("Finished in %s seconds" % (time.time() - start_time))
