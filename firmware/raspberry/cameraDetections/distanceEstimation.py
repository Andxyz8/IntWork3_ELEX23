import cv2 as cv
from cv2 import aruco
import numpy as np

def detectAruko():

    calib_data_path = r"D:\Users\icego\Documents\MultiMatrix.npz"

    calib_data = np.load(calib_data_path)
    # print(calib_data.files)
    cam_mat = calib_data["camMatrix"]
    dist_coef = calib_data["distCoef"]
    r_vectors = calib_data["rVector"]
    t_vectors = calib_data["tVector"]

    MARKER_SIZE = 8  

    marker_dict = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)

    param_markers = aruco.DetectorParameters()

    cap = cv.VideoCapture(0) #give the server id shown in IP webcam App

    # Variáveis para controle da detecção
    # detected_count = 0
    # required_consecutive_frames = 3

    # while True:
    ret, frame = cap.read()
    # if not ret:
    #     break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    if marker_corners:
        # Incrementar o contador de detecção
        # detected_count += 1
        # if detected_count >= required_consecutive_frames:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, MARKER_SIZE, cam_mat, dist_coef
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

                return 1, center_x - centerTela_x, distance
    else:
        # Redefinir o contador se o marcador não for detectado neste frame
        detected_count = 0
        return 0, 0, 0

    # cv.imshow("frame", frame)
    # key = cv.waitKey(0)
    # if key == ord("q"):
    #     break

    # cap.release()
    # cv.destroyAllWindows()

