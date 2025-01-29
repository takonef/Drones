import cv2

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)


def recognize_marker_get_center(frame, marker_id):
    global detector
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame_gray)

    if ids is None:
        return None, None

    if len(ids) != 1 or ids[0] != marker_id:
        return None, None

    marker_x_center = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]) // 4
    marker_y_center = (corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]) // 4

    return marker_x_center, marker_y_center


def is_marker_in_center_area(frame, marker_id, frame_center_x, frame_center_y):
    marker_x_center, maker_y_center = recognize_marker_get_center(frame, marker_id)

    window_for_marker = 50  # окно для маркера в пикселях
    cv2.rectangle(frame, (frame_center_x - window_for_marker, frame_center_y - window_for_marker),
                  (frame_center_x + window_for_marker, frame_center_y + window_for_marker), (0, 0, 255), 2)

    if marker_x_center is None:
        return False

    if (abs(marker_x_center - frame_center_x) <= window_for_marker and
            abs(maker_y_center - frame_center_y) <= window_for_marker):
        return True
    else:
        return False


def stabilize_at_marker(frame, frame_center_x, frame_center_y):
    frame, dVx_aruco, dVy_aruco, dx, dy, ids = aruco_detected(frame, frame_center_x, frame_center_y)
    ch_3 = ch_4 = 1500
    if dVx_aruco is not None and dVy_aruco is not None:
        color_for_arrow = (255, 0, 0)
        frame = cv2.arrowedLine(frame, (frame_center_x, frame_center_y),
                                (frame_center_x + dx, frame_center_y + dy), color_for_arrow, 2)
        ch_3 += int(dVy_aruco)
        ch_4 += int(dVx_aruco)

    return frame, ch_3, ch_4


def aruco_detected(frame, xc, yc):
    # TODO использовать функцию recognize_marker_get_center
    global detector
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame_gray)
    dVy_aruco = None
    dVx_aruco = None
    dx, dy = 0, 0
    if ids is not None:
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        aruco_xc = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]) // 4
        aruco_yc = (corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]) // 4
        dx = int(-(xc - aruco_xc))
        dy = int(-(yc - aruco_yc))

        dV_aruco = 120  # 200
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
    return frame, dVx_aruco, dVy_aruco, dx, dy, ids
