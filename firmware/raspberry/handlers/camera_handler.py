"""Module that contains the class to handle camera controlling.

- Handles the camera servo motor to rotate the camera.
- Handles the algorithms to perform face recognition.
- Handles the algorithms to perform movement detection.
"""
# pylint: disable = E1101:no-member, E0611:no-name-in-module, E0401:import-error
from time import time as this_moment
from uuid import uuid4 as generate_unique_id
import numpy as np
import cv2 as cv
from cv2 import (
    VideoCapture,
    createBackgroundSubtractorMOG2,
    resize,
    waitKey,
    threshold,
    erode,
    dilate,
    findContours,
    contourArea,
    boundingRect,
    rectangle,
    putText,
    imwrite,
    # imshow,
    # destroyAllWindows,
    THRESH_BINARY,
    RETR_EXTERNAL,
    CHAIN_APPROX_SIMPLE,
    FONT_HERSHEY_SIMPLEX
)
from handlers.esp_communication import ESPCommunicationHandler

class CameraHandler:

    def __init__(self) -> None:
        self.__last_image_unique_id: str = ""

    @property
    def last_image_unique_id(self) -> str:
        """Return the last image unique id.
        """
        return self.__last_image_unique_id

    def __save_image_locally(self, image_to_save) -> None:
        """Save the image locally.
        """
        self.__last_image_unique_id = str(generate_unique_id())

        path_image_to_save = f"handlers/.imgs/{self.__last_image_unique_id}.jpeg"

        imwrite(path_image_to_save, image_to_save)

    def __detect_movement(self, duration: int) -> bool:
        cap = VideoCapture(0)

        fgbg = createBackgroundSubtractorMOG2(detectShadows = True)

        # Initial time
        start_time = this_moment()

        movement_detected = False

        while (this_moment() - start_time) < start_time + duration:
            success_capturing, image_captured = cap.read()

            # Check if we get the frame
            if success_capturing:
                image_captured = resize(image_captured, (600, 500))
                waitKey(30)
                fgmask = fgbg.apply(image_captured)
                _, thresh = threshold(fgmask.copy(), 180, 255, THRESH_BINARY)
                # creating a kernel of 4*4
                kernel = np.ones((7, 7), np.uint8)
                # applying errosion to avoid any small motion in video
                thresh = erode(thresh, kernel)
                # dilating our image
                thresh = dilate(thresh, None, iterations=6)

                # finding the contours, we are not using the hierarchy return
                contours, _ = findContours(
                    thresh,
                    RETR_EXTERNAL,
                    CHAIN_APPROX_SIMPLE
                )

                for contour in contours:
                    # finding area of contour
                    area = contourArea(contour)
                    # print(area)
                    # if area greater than the specified value the only then we will consider it
                    if area > 1200 and this_moment() - start_time > 1:
                        movement_detected = True
                        # find the rectangle co-ordinates
                        x, y, w, h = boundingRect(contour)
                        # and then dra it to indicate the moving object
                        rectangle(image_captured, (x, y), (x + w, y + h), (255, 0, 255), 3)

                        # Insert text in the image to indicate which part triggered the alarm
                        putText(
                            img = image_captured,
                            text = 'MOTION DETECTED',
                            org = (x, y - 5),
                            fontFace = FONT_HERSHEY_SIMPLEX,
                            fontScale = 0.5,
                            color = (255, 0, 0),
                            thickness = 2
                        )

                        # Save the image locally before send to cloud storage database
                        self.__save_image_locally(image_captured)

                # imshow('frame',img)
                # imshow('frame2', thresh)
                if movement_detected:
                    break

            else:
                break

        cap.release()
        # destroyAllWindows()
        return movement_detected

    def __detect_face(self) -> bool:
        # Inicializar a câmera
        cap = cv.VideoCapture(0)
    
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
        cv.imwrite("image.jpg", frame)

        # Liberar a câmera
        cap.release()

        # TODO: chage this two paths in the raspberry pi
        # Load YOLO model
        net = cv.dnn.readNet("./yolov3.weights", "./yolov3.cfg")

        # Define input image
        image = cv.imread("image.jpg")

        # Get image dimensions
        (height, width) = image.shape[:2]

        # Define the neural network input
        blob = cv.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
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
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv.imwrite("personDetection.jpg", image)
        # Save the image locally before send to cloud storage database
        self.__save_image_locally(image)

        if not people:
            return False
        return True

    def __detect_aruco_marker(self) -> tuple:
        #TODO: change this path in the raspberry pi
        calib_data_path = r"D:\Users\icego\Documents\MultiMatrix.npz"

        calib_data = np.load(calib_data_path)
        # print(calib_data.files)
        cam_mat = calib_data["camMatrix"]
        dist_coef = calib_data["distCoef"]
        r_vectors = calib_data["rVector"]
        t_vectors = calib_data["tVector"]

        MARKER_SIZE = 8

        marker_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)

        param_markers = cv.aruco.DetectorParameters_create()

        cap = cv.VideoCapture(0) #give the server id shown in IP webcam App

        ret, frame = cap.read()

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, reject = cv.aruco.detectMarkers(
            gray_frame, marker_dict, parameters=param_markers
        )

        if marker_corners:
            # Incrementar o contador de detecção
            # detected_count += 1
            # if detected_count >= required_consecutive_frames:
            rVec, tVec, _ = cv.aruco.estimatePoseSingleMarkers(
                marker_corners,
                MARKER_SIZE,
                cam_mat,
                dist_coef
            )
            total_markers = range(0, marker_IDs.size)
            for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                cv.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                )
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left = corners[3].ravel()

                # Calcular a distância
                distance = np.sqrt(
                    tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
                )

                # Calcular o centro do marcador
                center_x = int((corners[0][0] + corners[2][0]) / 2)
                center_y = int((corners[0][1] + corners[2][1]) / 2)

                height, width, _ = frame.shape
                centerTela_x = width // 2
                centerTela_y = height // 2

                # Exibir informações
                point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
                cv.putText(
                    frame,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    top_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"x:{round(center_x - centerTela_x,1)} y: {round(center_y - centerTela_y,1)} ",
                    bottom_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )

                return True, center_x - centerTela_x, distance, ids[0]
        else:
            # Redefinir o contador se o marcador não for detectado neste frame
            detected_count = 0
            return False, 0, 0, 0

    def __reposition_aruco_reference(
        self,
        center_dist: int,
        linear_dist: float,
        ctrl_esp: ESPCommunicationHandler
    ) -> bool:
        # TODO: implement this function
        return True

    def movement_face_detection_routine(self, ctrl_esp: ESPCommunicationHandler) -> bool:
        ctrl_esp.center_camera_servo()

        movement_detected = self.__detect_movement(5)
        if movement_detected:
            return "movement detected"

        face_detected = self.__detect_face()
        if face_detected:
            return "face detected"

        ctrl_esp.rotate_camera_servo_right()

        self.__detect_movement(5)
        if movement_detected:
            return "movement detected"

        face_detected = self.__detect_face()
        if face_detected:
            return "face detected"

        ctrl_esp.rotate_camera_servo_left()

        self.__detect_movement(5)
        if movement_detected:
            return "movement detected"

        face_detected = self.__detect_face()
        if face_detected:
            return "face detected"

        ctrl_esp.center_camera_servo()
        return "nothing detected"

    def read_aruco_marker_routine(self, ctrl_esp: ESPCommunicationHandler) -> int:
        """Read the aruco marker and return the id of the marker.

        Args:
            ctrl_esp (ESPCommunicationHandler): instance to handle the communication
                with the ESP.

        Returns:
            int: id of the aruco marker.
        """
        detected = False

        success = ctrl_esp.center_camera_servo()
        while not success:
            success = ctrl_esp.center_camera_servo()

        detected, center_dist, linear_dist, id_aruco = self.__detect_aruco_marker()
        if detected:
            self.__reposition_aruco_reference(center_dist, linear_dist, ctrl_esp)
            return id_aruco

        success = ctrl_esp.rotate_camera_servo_right()
        while not success:
            success = ctrl_esp.rotate_camera_servo_right()

        detected, center_dist, linear_dist, id_aruco = self.__detect_aruco_marker()
        if detected:
            self.__reposition_aruco_reference(center_dist, linear_dist, ctrl_esp)
            return id_aruco

        success = ctrl_esp.rotate_camera_servo_left()
        while not success:
            success = ctrl_esp.rotate_camera_servo_left()

        detected, center_dist, linear_dist, id_aruco = self.__detect_aruco_marker()
        if detected:
            self.__reposition_aruco_reference(center_dist, linear_dist, ctrl_esp)
            return id_aruco
        return 0

# pylint: enable = E1101:no-member, E0611:no-name-in-module, E0401:import-error
