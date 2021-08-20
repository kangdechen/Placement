import imghdr
import os


import datetime
import random
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, session
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image
import  numpy as np
import cv2
from PIL import Image
import  DataBase.get_data as db

from DataBase.Config import GetConnection

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'
class_names =['Apple Braeburn', 'Apple Crimson Snow', 'Apple Golden 1', 'Apple Golden 2', 'Apple Golden 3', 'Apple Granny Smith', 'Apple Pink Lady', 'Apple Red 1', 'Apple Red 2', 'Apple Red 3', 'Apple Red Delicious', 'Apple Red Yellow 1', 'Apple Red Yellow 2', 'Apricot', 'Avocado', 'Avocado ripe', 'Banana', 'Banana Lady Finger', 'Banana Red', 'Beetroot', 'Blueberry', 'Cactus fruit', 'Cantaloupe 1', 'Cantaloupe 2', 'Carambula', 'Cauliflower', 'Cherry 1', 'Cherry 2', 'Cherry Rainier', 'Cherry Wax Black', 'Cherry Wax Red', 'Cherry Wax Yellow', 'Chestnut', 'Clementine', 'Cocos', 'Corn', 'Corn Husk', 'Cucumber Ripe', 'Cucumber Ripe 2', 'Dates', 'Eggplant', 'Fig', 'Ginger Root', 'Granadilla', 'Grape Blue', 'Grape Pink', 'Grape White', 'Grape White 2', 'Grape White 3', 'Grape White 4', 'Grapefruit Pink', 'Grapefruit White', 'Guava', 'Hazelnut', 'Huckleberry', 'Kaki', 'Kiwi', 'Kohlrabi', 'Kumquats', 'Lemon', 'Lemon Meyer', 'Limes', 'Lychee', 'Mandarine', 'Mango', 'Mango Red', 'Mangostan', 'Maracuja', 'Melon Piel de Sapo', 'Mulberry', 'Nectarine', 'Nectarine Flat', 'Nut Forest', 'Nut Pecan', 'Onion Red', 'Onion Red Peeled', 'Onion White', 'Orange', 'Papaya', 'Passion Fruit', 'Peach', 'Peach 2', 'Peach Flat', 'Pear', 'Pear 2', 'Pear Abate', 'Pear Forelle', 'Pear Kaiser', 'Pear Monster', 'Pear Red', 'Pear Stone', 'Pear Williams', 'Pepino', 'Pepper Green', 'Pepper Orange', 'Pepper Red', 'Pepper Yellow', 'Physalis', 'Physalis with Husk', 'Pineapple', 'Pineapple Mini', 'Pitahaya Red', 'Plum', 'Plum 2', 'Plum 3', 'Pomegranate', 'Pomelo Sweetie', 'Potato Red', 'Potato Red Washed', 'Potato Sweet', 'Potato White', 'Quince', 'Rambutan', 'Raspberry', 'Redcurrant', 'Salak', 'Strawberry', 'Strawberry Wedge', 'Tamarillo', 'Tangelo', 'Tomato 1', 'Tomato 2', 'Tomato 3', 'Tomato 4', 'Tomato Cherry Red', 'Tomato Heart', 'Tomato Maroon', 'Tomato Yellow', 'Tomato not Ripened', 'Walnut', 'Watermelon']
food_class=['apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles']
def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')
@app.route("/")
def homepage():
    return render_template("index.html", title="HOME PAGE")

@app.route('/getupload/<filename>')
def upload_f(filename):
    file =  filename

    predict_name=predict_test(filename)

    return render_template('Uploaded.html', files=file,result=predict_name)
def create_uuid():
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");
        randomNum = random.randint(0, 100);
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum;

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        name = filename.split('.')[0]
        ext = filename.rsplit('.', 1)[1]
        new_url = name +create_uuid()+'.'+ext
        print(new_url)

        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], new_url))
    return redirect('/getupload/'+new_url)

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)



def predict_test(filename):
    # img = Image.open('uploads/34_100.jpg')  # 读取图片
    img = cv2.imread('uploads/' + filename)
    # resize图片大小 先将原本的(224,222,3) ---> (28,28,3)
    pred_img = cv2.resize(img, (224, 224))
    # 转换np数组格式
    pred_img = np.array(pred_img)
    # 重新reshape图片
    pred_img = pred_img.reshape(-1, 224, 224, 3)
    # 查看reshape后的图片shape
    print(pred_img.shape)
    # turn img to numpy tensor
    model = tf.keras.models.load_model("models/cnn_fv_food.h5")
    outputs = model.predict(pred_img)  # 将图片输入模型得到结果
    result_index = int(np.argmax(outputs))
    result = food_class[result_index]  # 获得对应的水果名称

    print(result)
    return result

    return result

@app.route('/uploads/camera')
def camera():

    cap = cv2.VideoCapture(0)  # 打开摄像头

    while (1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)  # 生成摄像头窗口

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下q 就截图保存并退出
            cv2.imwrite("C:/Users/a0023/PycharmProjects/MasterProject/uploads/temp"+create_uuid()+".jpg", frame)  # 保存路径
            break

    cap.release()
    cv2.destroyAllWindows()

    # 将图片处理成指定的格式 这里为299*299

    return redirect(url_for('upload_files'))

@app.route('/Loggin', methods=['GET', 'POST'])
def Loggin():
    msg = ''
    c = GetConnection()
    name = request.form['name']
    pwd = request.form['pwd']
    print(f'user name is {name}  and password is {pwd}')
    account = db.User.UserLogin(c,name,pwd)
    if account:
        session['loggedin'] = True
        session['id'] = int(account[0])
        session['username'] = account[1]



        return render_template('Upload.html')

    else:
        msg = 'null'
        return msg

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page

    return render_template('index.html')

@app.route('/getmeal/<name>')
def getfoodNuitri(name):
    c = GetConnection()
    name=request.args.get('name')
    list=db.Food.getDetectFood(c,name)
    print(list)
    return render_template('Uploaded.html',meals=list)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0', port='8888')
    #predict_test()
    #camera()
    #getfoodNuitri()
