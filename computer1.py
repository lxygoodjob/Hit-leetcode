import os
import pyautogui
import keyboard
import requests


url = "http://XXXXX:9210/get_code"

savefolder = './filesfolder'

def get_screen_and_rquest_llm():
    print('start screenshot !')
    x, y = pyautogui.position()
    img = pyautogui.screenshot(region=[0,0,x,y]) # x,y,w,h
    img_save_path = os.path.join(savefolder, 'screenshot.png')
    img.save(img_save_path)
    files={'input_file': open(img_save_path,'rb')}
    response = requests.request("POST", url, files=files)
    if response.json()['msg'] == 'success':
        print('please see the computer2 screen and get code !')
    else:
        print('please "Shift+Z" get new img or use "Shift+R" get code again !')

## don't screenshot, continue ocr the old picture
def get_code_again():
    img_save_path = os.path.join(savefolder, 'screenshot.png')
    files={'input_file': open(img_save_path,'rb')}
    response = requests.request("POST", url, files=files)
    if response.json()['msg'] == 'success':
        print('please see the computer2 screen and get code !')
    else:
        print('please "Shift+Z" get new img or use "Shift+R" get code again !')


keyboard.add_hotkey('Shift+Z', get_screen_and_rquest_llm)
keyboard.add_hotkey('Shift+X', get_code_again)


# 进入监听状态
try:
    keyboard.wait('ctrl+c')
except KeyboardInterrupt:
    pass