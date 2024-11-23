import tensorflow as tf
import numpy as np
from PIL import Image


# 이미지로 상태 분석
# input : 이미지 경로
# output : True(정상) , False(비정상)
def model_predict(img_path):
    interpreter = tf.lite.Interpreter(model_path="convert_model.tflite")
    interpreter.allocate_tensors()

    # 입/출력 텐서 가져오기
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 이미지 전처리
    image = Image.open(img_path).convert("RGB")
    image = image.resize((224, 224))
    input_data = np.expand_dims(np.array(image) / 255.0, axis=0)
    input_data = (input_data - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]

    # 추론 시작~
    interpreter.set_tensor(input_details[0]['index'], input_data.astype(np.float32))
    interpreter.invoke()

    # 결과 처리
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output_data)
    #print(f"Predict Result : {predicted_class}")
    #print(f"Confidences : {output_data}")

    return True if predicted_class == 0 else False

