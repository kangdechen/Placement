import cv2
import numpy as np

import xml.dom.minidom
import os
import argparse


def main():
    # JPG文件的地址
    img_path = 'output/train/'
    # XML文件的地址
    anno_path = 'output/json'
    # 存结果的文件夹
    cut_path = 'output/'
    # 获取文件夹中的文件
    imagelist = os.listdir(img_path)

    for image in imagelist:
        image_pre, ext = os.path.splitext(image)
        img_file = img_path + image
        # 读取图片
        img = cv2.imread(img_file)
        xml_file = anno_path + image_pre + '.xml'
        # 打开xml文档
        DOMTree = xml.dom.minidom.parse(xml_file)
        # 得到文档元素对象
        with open("./label.txt", "w+") as f:  # 打开文件
            for filename in os.listdir(label_path):
                # 定义特征点
                x1, y1 = 0, 0  # 框左上  x: 距左，y:距上
                x2, y2 = 0, 0  # 框右下
                mark_x1, mark_y1 = 0, 0  # 左上点
                mark_x2, mark_y2 = 0, 0  # 右上点
                mark_x3, mark_y3 = 0, 0  # 左下点
                mark_x4, mark_y4 = 0, 0  # 右下点
                if filename.endswith(".json"):
                    json_path = os.path.join(label_path, filename)
                    data = json.load(open(json_path, 'r'))

                    img_name = data['imagePath']  # 拿到图像的名字

                    for obj in data['shapes']:
                        if obj['label'] == "box":  # 框
                            x1 = int(obj['points'][0][0])
                            y1 = int(obj['points'][0][1])
                            x2 = int(obj['points'][1][0])
                            y2 = int(obj['points'][1][1])
                        if obj['label'] == "left_up":  # 左上点
                            mark_x1 = int(obj['points'][0][0])
                            mark_y1 = int(obj['points'][0][1])
                        if obj['label'] == "right_up":  # 右上点
                            mark_x2 = int(obj['points'][0][0])
                            mark_y2 = int(obj['points'][0][1])
                        if obj['label'] == "left_down":  # 左下点
                            mark_x3 = int(obj['points'][0][0])
                            mark_y3 = int(obj['points'][0][1])
                        if obj['label'] == "right_down":  # 右下点
                            mark_x4 = int(obj['points'][0][0])
                            mark_y4 = int(obj['points'][0][1])

                    # 保存图片
                    img = Image.open(os.path.join(label_path, img_name))
                    img_save_path = os.path.join(save_path, img_name)
                    img.save(img_save_path)

                    # 写入文件
                    line = "{0} {1} {2} {3} {4} " \
                           "{5} {6} {7} {8} " \
                           "{9} {10} {11} {12}\n".format(img_save_path, x1, y1, x2, y2,
                                                         mark_x1, mark_y1, mark_x2, mark_y2,
                                                         mark_x3, mark_y3, mark_x4, mark_y4)
                    f.write(line)

if __name__ == '__main__':
    main()