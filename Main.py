import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image
import  numpy as np
import  cv2
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'
class_names =['Apple Braeburn', 'Apple Crimson Snow', 'Apple Golden 1', 'Apple Golden 2', 'Apple Golden 3', 'Apple Granny Smith', 'Apple Pink Lady', 'Apple Red 1', 'Apple Red 2', 'Apple Red 3', 'Apple Red Delicious', 'Apple Red Yellow 1', 'Apple Red Yellow 2', 'Apricot', 'Avocado', 'Avocado ripe', 'Banana', 'Banana Lady Finger', 'Banana Red', 'Beetroot', 'Blueberry', 'Cactus fruit', 'Cantaloupe 1', 'Cantaloupe 2', 'Carambula', 'Cauliflower', 'Cherry 1', 'Cherry 2', 'Cherry Rainier', 'Cherry Wax Black', 'Cherry Wax Red', 'Cherry Wax Yellow', 'Chestnut', 'Clementine', 'Cocos', 'Corn', 'Corn Husk', 'Cucumber Ripe', 'Cucumber Ripe 2', 'Dates', 'Eggplant', 'Fig', 'Ginger Root', 'Granadilla', 'Grape Blue', 'Grape Pink', 'Grape White', 'Grape White 2', 'Grape White 3', 'Grape White 4', 'Grapefruit Pink', 'Grapefruit White', 'Guava', 'Hazelnut', 'Huckleberry', 'Kaki', 'Kiwi', 'Kohlrabi', 'Kumquats', 'Lemon', 'Lemon Meyer', 'Limes', 'Lychee', 'Mandarine', 'Mango', 'Mango Red', 'Mangostan', 'Maracuja', 'Melon Piel de Sapo', 'Mulberry', 'Nectarine', 'Nectarine Flat', 'Nut Forest', 'Nut Pecan', 'Onion Red', 'Onion Red Peeled', 'Onion White', 'Orange', 'Papaya', 'Passion Fruit', 'Peach', 'Peach 2', 'Peach Flat', 'Pear', 'Pear 2', 'Pear Abate', 'Pear Forelle', 'Pear Kaiser', 'Pear Monster', 'Pear Red', 'Pear Stone', 'Pear Williams', 'Pepino', 'Pepper Green', 'Pepper Orange', 'Pepper Red', 'Pepper Yellow', 'Physalis', 'Physalis with Husk', 'Pineapple', 'Pineapple Mini', 'Pitahaya Red', 'Plum', 'Plum 2', 'Plum 3', 'Pomegranate', 'Pomelo Sweetie', 'Potato Red', 'Potato Red Washed', 'Potato Sweet', 'Potato White', 'Quince', 'Rambutan', 'Raspberry', 'Redcurrant', 'Salak', 'Strawberry', 'Strawberry Wedge', 'Tamarillo', 'Tangelo', 'Tomato 1', 'Tomato 2', 'Tomato 3', 'Tomato 4', 'Tomato Cherry Red', 'Tomato Heart', 'Tomato Maroon', 'Tomato Yellow', 'Tomato not Ripened', 'Walnut', 'Watermelon']

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('Upload.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('upload_files'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/predict/<filename>')
def predict_img(filename):
    # img = Image.open('uploads/34_100.jpg')  # 读取图片
    img = cv2.imread('uploads/',filename)
    # resize图片大小 先将原本的(224,222,3) ---> (28,28,3)
    pred_img = cv2.resize(img, (224, 224))
    # 转换np数组格式
    pred_img = np.array(pred_img)
    # 重新reshape图片
    pred_img = pred_img.reshape(-1, 224, 224, 3)
    # 查看reshape后的图片shape
    print(pred_img.shape)
    # turn img to numpy tensor
    model = tf.keras.models.load_model("models/cnn_fv.h5")
    outputs = model.predict(pred_img)  # 将图片输入模型得到结果
    result_index = int(np.argmax(outputs))
    result = class_names[result_index]  # 获得对应的水果名称

    print(result)
    return result # 在界面上做显示

def predict_test():


    #img = Image.open('uploads/34_100.jpg')  # 读取图片
    img =cv2.imread('uploads/34_100.jpg')
    # resize图片大小 先将原本的(224,222,3) ---> (28,28,3)
    pred_img = cv2.resize(img, (224, 224))
    # 转换np数组格式
    pred_img = np.array(pred_img)
    # 重新reshape图片
    pred_img = pred_img.reshape(-1, 224, 224, 3)
    # 查看reshape后的图片shape
    print(pred_img.shape)
    # turn img to numpy tensor
    model = tf.keras.models.load_model("models/cnn_fv.h5")
    outputs = model.predict(pred_img) # 将图片输入模型得到结果
    result_index = int(np.argmax(outputs))
    result = class_names[result_index]  # 获得对应的水果名称

    print(result)


    return result
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8888')
    #predict_test()