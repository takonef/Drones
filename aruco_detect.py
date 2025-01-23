import cv2
import numpy as np
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)


def aruco_detected(detector, frame, xc, yc):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame_gray)
    dVy_aruco = -1
    dVx_aruco = -1
    dx, dy = 0, 0
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        aruco_xc = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]) // 4
        aruco_yc = (corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]) // 4
        dx = int(-(xc - aruco_xc))
        dy = int(-(yc - aruco_yc))

        dV_aruco = 200
        dVx_aruco = dV_aruco * (dx / xc)
        dVy_aruco = dV_aruco * (dy / xc)

        limit = 100

        if dVx_aruco > limit:
            dVx_aruco = limit
        if dVx_aruco < -limit:
            dVx_aruco = -limit

        if dVy_aruco > limit:
            dVy_aruco = limit
        if dVy_aruco < -limit:
            dVy_aruco = -limit
    return (dVx_aruco, dVy_aruco, dx, dy)

