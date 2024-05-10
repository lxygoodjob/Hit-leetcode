from paddleocr import PaddleOCR
import numpy as np

# paddle weights
det_model_path = "./pp_weights/ch_PP-OCRv4_det_infer"
rec_model_path = "./pp_weights/ch_PP-OCRv4_rec_infer"
cls_model_path = "./pp_weights/ch_ppocr_mobile_v2.0_cls_slim_infer"

def ocr_init():
    paddle_ocr = PaddleOCR(use_angle_cls=True, lang='ch', 
                        det_model_dir=det_model_path, 
                        rec_model_dir=rec_model_path, 
                        cls_model_dir=cls_model_path,
                        det_limit_type='max',
                        drop_score=0.4)
    print('ocr init down !')
    return paddle_ocr

def check_merge(text1, text2):
    x1, y1, x2, y2, x3, y3, x4, y4 = text1[:8]
    p1, q1, p2, q2, p3, q3, p4, q4 = text2[:8]
    t1 = np.array(text1[:8]).reshape((-1, 2))
    t2 = np.array(text2[:8]).reshape((-1, 2))
    if min(t1[:, 0]) <= min(t2[:, 0]):
        top_border, bottom_border = max(y2, q1), min(y3, q4)
    else:
        top_border, bottom_border = max(q2, y1), min(q3, y4)
    
    center1 = (max(t1[:, 1]) + min(t1[:, 1])) / 2
    center2 = (max(t2[:, 1]) + min(t2[:, 1])) / 2

    if max(bottom_border,top_border) - min(bottom_border, top_border) >= \
        max(center1, center2) - min(center1, center2):
        merge = True
    else:
        merge = False
    return merge

def get_line_dict(coord_lists):
    for i in range(len(coord_lists)):
        t_ = np.array(coord_lists[i][:8]).reshape((-1, 2))
        centerx, centery = (max(t_[:, 0]) + min(t_[:, 0])) / 2, (max(t_[:, 1]) + min(t_[:, 1])) / 2
        coord_lists[i].extend([centerx, centery])
    coord_lists = sorted(coord_lists, key=lambda s: (s[-1], s[-2]))
    rec_dict = dict()
    rec_dict[0] = [coord_lists[0]]
    n = 0
    for i in range(1, len(coord_lists)):
        rec_dict[n] = sorted(rec_dict[n], key=lambda s: s[-2])
        merge = check_merge(rec_dict[n][-1], coord_lists[i])
        if merge:
            rec_dict[n].append(coord_lists[i])
        else:
            n += 1
            rec_dict[n] = [coord_lists[i]]
    return rec_dict

def ocr_infer(img_path, paddle_ocr):
    total_text = ''
    result = paddle_ocr.ocr(img_path, cls=True)
    texts = []
    for line_ in result:
        for line in line_:
            text = []
            bbox = np.array(line[0])
            bbox = bbox.reshape((-1)).tolist()
            t_ = line[1][0]
            text.extend(bbox)
            text.append(t_)
            texts.append(text)
    rec_dict = get_line_dict(texts)
    for key in rec_dict.keys():
        rec_dict[key] = sorted(rec_dict[key], key=lambda s: s[-2])
        lines = rec_dict[key]
        t_ = ''
        for item in lines:
            t_ += item[8]
        total_text += t_ + '\n'
    return total_text

if __name__ == '__main__':
    im = r'C:\Users\xiaoyuli\Desktop\task\screen_imgs\237d6db5-86ba-4f7b-9930-36936352c7ab.png'
    paddle_ocr = ocr_init()
    ocr_infer(im, paddle_ocr)