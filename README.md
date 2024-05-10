# 面试助手
面试助手，使用ocr+大模型反击八股文
## 快捷键信息
···
main.py
填上大模型api-key， 我用的智谱， 有条件的可用openai替换

keyboard.add_hotkey('Shift+Z', get_screen_and_ocr) # 截图并ocr, 这边需要先把鼠标移到要截取的区域右下角，会从屏幕左上角（0，0）截到该位置，并用ppocr识别
keyboard.add_hotkey('Shift+Tab', get_answer) # 送入大模型获取code，预置了一个提示词，你可以修改
keyboard.add_hotkey('Shift+R', reset_count) # 输出是一行一行输出，如果发现中间有误操作，可以reset, 从头开始
keyboard.add_hotkey('Enter', write_answer) # 按一次enter输出一行
···

本项目旨在反击无脑八股文面试。
