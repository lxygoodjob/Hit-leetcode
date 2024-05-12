import os
import json
import numpy as np
from flask import Flask, request, make_response
from utils.ocr_func import ocr_init, ocr_infer
from utils.call_llm import query_llm


########## flask func ##########
app = Flask(__name__)

class JsonEncoder(json.JSONEncoder):
    """Convert numpy classes to JSON serializable objects."""

    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)


def json_dumps(data):
    return json.dumps(data, ensure_ascii=False, cls=JsonEncoder)

def wrap_resp(res, status=400, headers={'Content-Type': 'application/json'}):
    resp = make_response(json_dumps(res), status)
    resp.headers = headers
    return resp

########## ocr init #########
paddle_ocr = ocr_init()

######### llm api key #########
key = "XXXXXX"
llm_type = "glm-4"

######## mian func ###########
savefolder = './filesfolder'

def ocr_screen_and_get_answer(image, out_folder):
    print('start ocr !')
    texts = ocr_infer(image, paddle_ocr)
    print('ocr down, start request llm !')
    command = query_llm(key, llm_type, texts)
    if '```python' in command:
        command = command.split('```python')[1].split('```')[0]
    elif '```' in command:
        command = command.split('```')[1].split('```')[0]
    else:
        print('the result is wrong, please query llm again !')
    print("~~温馨提示，代码已生成~~")
    with open(os.path.join(out_folder, 'result.txt'), 'w', encoding='utf-8') as fw:
        fw.write(command)
    print(command)
    return command

@app.route('/get_code', methods = ['POST'])
def get_code():
    inf = request.files.get('input_file')
    out_folder = os.path.join(savefolder, 'output')
    os.makedirs(out_folder, exist_ok=True)
    os.makedirs(savefolder, exist_ok=True)
    input_file = os.path.join(savefolder, inf.filename)
    inf.save(input_file)
    try:
        out = ocr_screen_and_get_answer(input_file, out_folder)
        res = {
            'msg': 'success',
            'code': 0,
            'data': out,
            }
        return wrap_resp(res, 200)
    except Exception as e:
        res = {
            'msg': 'fail',
            'code': -1,
            'data': str(e)
            }
        return wrap_resp(res)


if __name__ == '__main__':
    app.run('0.0.0.0', 9210, debug=False)


