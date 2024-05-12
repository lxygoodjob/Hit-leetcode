# 面试助手
面试助手, 使用ocr+大模型反击八股文, 使用本代码，你需要有两台电脑，一台面试用电脑用于获取屏幕截屏，一台用于请求大模型获取code，便于照着打字你输入（上一版本是自动输入，但是速度太快，不能模拟人的手速）  

## 快捷键信息

### 电脑2，获取答案用电脑
pip install -r requirements_computer2.txt  

填上api key 和 大模型类型（如果是openai，填对应的gpt的模型名）  
key = "xxxxx"  
llm_type = "glm-4"  

运行 python computer2.py  
获取当前的请求url， 一般是192.168.x.x:9210, 这里我设的端口是9210  


### 电脑1，面试用电脑
pip install -r requirements_computer1.txt

填入 电脑2运行后的url = "http://xxxx:9210/get_code"

运行 python computer1.py

快捷键 'Shift+Z'  
截图并请求答案, 这边需要先把鼠标移到要截取的区域右下角，会从屏幕左上角（0，0）截到该位置  

快捷键 'Shift+X'  
从新识别上一次的图片，重新请求大模型获取答案, 如果重新截图识别获取答案，请再次按快捷键 'Shift+Z' ， 注意鼠标位置！！！！！  

## 本项目旨在反击无脑八股文面试，请勿滥用哟
