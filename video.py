import cv2
from PIL import Image

cap = cv2.VideoCapture(0)  # 打开摄像头

while (1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)  # 生成摄像头窗口

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下q 就截图保存并退出
        cv2.imwrite("C:/Users/Administrator/Desktop/水果识别/te.jpg", frame)  # 保存路径
        break

cap.release()
cv2.destroyAllWindows()

# 将图片处理成指定的格式 这里为299*299
image = Image.open("C:/Users/Administrator/Desktop/水果识别/te.jpg")
image_size = image.resize((299, 299), Image.ANTIALIAS)
image_size.save("C:/Users/Administrator/Desktop/水果识别/ta.jpg")