import random

import cv2
import numpy as np
from ultralytics import YOLO

def detectPersonV8():
    people = False

    # opening the file in read mode
    my_file = open("./coco.txt", "r")
    # reading the file
    data = my_file.read()
    # replacing end splitting the text | when newline ('\n') is seen.
    class_list = data.split("\n")
    my_file.close()

    # print(class_list)

    # Generate random colors for class list
    detection_colors = []
    for i in range(len(class_list)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        detection_colors.append((b, g, r))

    # load a pretrained YOLOv8n model
    model = YOLO("./yolov8n.pt", "v8")

    # Vals to resize video frames | small frame optimise the run
    frame_wid = 640
    frame_hyt = 480

    # Inicializar a câmera
    cap = cv2.VideoCapture(0)

    # Verificar se a câmera foi aberta corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        exit()

    # Capturar um quadro (frame) da câmera
    ret, frame = cap.read()

    # Verificar se o quadro foi capturado corretamente
    if not ret:
        print("Erro ao capturar o frame.")
        cap.release()
        exit()

    # Salvar o quadro como "image.jpg"
    cv2.imwrite("image.jpg", frame)

    # Liberar a câmera
    cap.release()

    # Get image dimensions
    (height, width) = frame.shape[:2]

    #  resize the frame | small frame optimise the run
    # frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.45, save=False)

    # Convert tensor array to numpy
    DP = detect_params[0].numpy()
    # print(DP)

    if len(DP) != 0:
        for i in range(len(detect_params[0])):
            # print(i)

            
            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            if int(clsID) == 0 and conf > 0.5:
                people = True

                bb = box.xyxy.numpy()[0]

                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    detection_colors[int(clsID)],
                    3,
                )

                # Display class name and confidence
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    frame,
                    class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )
                cv2.imwrite("personDetection.jpg", frame)

    # Display the resulting frame
    # cv2.imshow("ObjectDetection", frame)

    # Especificar a largura desejada para exibição
    # desired_width = 800

    # Calcular a proporção de redimensionamento
    # scale_ratio = desired_width / float(width)

    # Redimensionar a imagem
    # resized_image = cv2.resize(frame, (int(desired_width), int(height * scale_ratio)))

    # Mostrar a imagem redimensionada
    # cv2.imshow("Resized Image", resized_image)

    # Terminate run when "Q" pressed
    # cv2.waitKey(0)

    # When everything done, release the capture
    # cap.release()
    # cv2.destroyAllWindows()

    if not people:
        return False
    else:
        return True
