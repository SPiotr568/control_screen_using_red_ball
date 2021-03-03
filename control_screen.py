import cv2 
import numpy as np
import pyautogui

camera = cv2.VideoCapture(0)

red_floor = np.array([140, 90, 120], np.uint8)
red_ceil = np.array([180, 255, 255], np.uint8)

last_y = 0
last_x = 0
flag_visible_ball = False

def scroll(y):
    diff = last_y - y
    if abs(diff) > 10 and last_y != 0:
        pyautogui.scroll((diff-10)/3)

def change_tab(x):
    diff = last_x - x
    if diff > 100 and last_x != 0:
        pyautogui.hotkey('ctrl', 'tab')

while True:
    ret, frame = camera.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv_frame, red_floor, red_ceil)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    flag_visible_ball = False
    for c in contours:
        area = cv2.contourArea(c)
        if area > 800:
            flag_visible_ball = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.drawContours(frame, c, -1, (0,0,255), 2)
            scroll(y)
            change_tab(x)
            last_y = y
            last_x = x
    if flag_visible_ball == False:
        last_y = 0
        last_x = 0

    cv2.imshow('Screen controller',frame)
    cv2.imshow('Red mask',red_mask)

    if cv2.waitKey(10) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()