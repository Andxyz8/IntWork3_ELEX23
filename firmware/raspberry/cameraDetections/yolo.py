import cv2
import numpy as np

def detectPerson():
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

    # Load YOLO model
    net = cv2.dnn.readNet("./yolov3.weights", "./darknet/cfg/yolov3.cfg")

    # Define input image
    image = cv2.imread("image.jpg")

    # Get image dimensions
    (height, width) = image.shape[:2]

    # Define the neural network input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward propagation
    output_layer_name = net.getUnconnectedOutLayersNames()
    output_layers = net.forward(output_layer_name)

    # Initialize list of detected people
    people = []

    # Loop over the output layers
    for output in output_layers:
        # Loop over the detections
        for detection in output:
            # Extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only keep detections with a high confidence
            if class_id == 0 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Add the detection to the list of people
                people.append((x, y, w, h))

    # Draw bounding boxes around the people
    for (x, y, w, h) in people:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite("personDetection.jpg", image)

    # Especificar a largura desejada para exibição
    # desired_width = 800

    # Calcular a proporção de redimensionamento
    # scale_ratio = desired_width / float(width)

    # Redimensionar a imagem
    # resized_image = cv2.resize(image, (int(desired_width), int(height * scale_ratio)))

    # Mostrar a imagem redimensionada
    # cv2.imshow("Resized Image", resized_image)
    # cv2.waitKey(0)
    if not people:
        return False
    else:
        return True
    