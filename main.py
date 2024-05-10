import os
import pyautogui
import keyboard
from ocr_func import ocr_init, ocr_infer
from call_llm import query_llm

paddle_ocr = ocr_init()
key = ""

savefolder = './filesfolder'
count = 0

def get_screen_and_ocr():
    print('start ocr !')
    x, y = pyautogui.position()
    img = pyautogui.screenshot(region=[0,0,x,y]) # x,y,w,h
    img_save_path = os.path.join(savefolder, 'screenshot.png')
    img.save(img_save_path)
    texts = ocr_infer(img_save_path, paddle_ocr)
    ocr_result_save_path = os.path.join(savefolder, 'ocr_result.txt')
    with open(ocr_result_save_path, 'w', encoding='utf-8') as fw:
        fw.write(texts)
    print('ocr down !')

    return ocr_result_save_path

def get_answer():
    print('start request llm !')
    x, y = pyautogui.position()
    with open(os.path.join(savefolder, 'ocr_result.txt'), "r", encoding='utf-8') as fr:
        texts = fr.read()
    command = query_llm(key, "glm-4", texts)
    if '```python' in command:
        command = command.split('```python')[1].split('```')[0]
    elif '```' in command:
        command = command.split('```')[1].split('```')[0]
    else:
        print('the result is wrong, please query llm again !')
    print('preview result: ', command)
    with open(os.path.join(savefolder, 'answer.txt'), 'w', encoding='utf-8') as fw:
        fw.write(command)
    print('query llm down !')

    return command

def write_answer():
    global count
    print('start write line :', count)
    with open(os.path.join(savefolder, 'answer.txt'), "r", encoding='utf-8') as fr:
        command = fr.read()
    command_list = command.split('\n')
    # command_list = [char.strip() for char in command.split('\n')]
    pyautogui.write(command_list[count], interval=0.15)
    count += 1
    return command_list[count]

def reset_count():
    global count
    count = 0

keyboard.add_hotkey('Shift+Z', get_screen_and_ocr)
keyboard.add_hotkey('Shift+Tab', get_answer)
keyboard.add_hotkey('Shift+R', reset_count)
keyboard.add_hotkey('Enter', write_answer)

# 进入监听状态
try:
    keyboard.wait('ctrl+c')
except KeyboardInterrupt:
    pass
