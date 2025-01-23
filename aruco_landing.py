from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time
# from line_trace_top_bottom import *
from line_only_top import *


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

nearby_pixels = 61
edge = 15
if __name__ == "__main__":
    print(
        """
    1 -- arm
    2 -- disarm
    3 -- takeoff
    4 -- land

    ↶q  w↑  e↷    i-↑
    ←a      d→     k-↓
        s↓"""
    )
    is_control_by_PID = False
    centered = False
    pioneer_mini = Pioneer()
    camera = Camera()
    min_v = 1300
    max_v = 1700
    counter_land = 0
    try:
        while True:
            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000
            frame = camera.get_cv_frame()



            if frame is None:
                continue

            yc, xc, _ = frame.shape
            yc //= 2
            xc //= 2
            yc -= 1
            xc -= 1

            target_circle_x, frame_after_thresh, dx_center, dangle = get_black_line(frame, nearby_pixels, edge)

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect the markers
            corners, ids, rejected = detector.detectMarkers(frame_gray)
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)

                aruco_xc = (corners[0][0][0] + corners[0][1][0] + corners[0][2][0] + corners[0][3][0]) // 4
                aruco_yc = (corners[0][0][1] + corners[0][1][1] + corners[0][2][1] + corners[0][3][1]) // 4

                dx = -(xc - aruco_xc)
                dy = -(yc - aruco_yc)

                print("dx, dy", dx, dy)

                color_for_arrow = (255, 0, 0)
                    # if is_control_by_PID:
                    #     color_for_arrow = (0, 255, 0)
                frame = cv2.arrowedLine(frame, (xc, yc), (xc + dx, yc + dy), color_for_arrow, 2)

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

                # print("dVx, dVy", dVx, dVy)

                counter_land = 1
                ch_3 = 1500 + int(dVy_aruco)
                ch_4 = 1500 + int(dVx_aruco)
                ch_1 = 1350 #вниз
            elif counter_land == 1:
                pioneer_mini.land()


            dV_max = 300
            dVx = dV_max * (dx_center / xc)
            # print(dangle)

            dVrot_k = 250

            limit = 170
            if dVx > limit:
                dVx = limit
            if dVx < -limit:
                dVx = -limit

            if not is_control_by_PID:
                dx = 0
                color = [0, 0, 255]
            else:
                if target_circle_x == 0:
                    is_control_by_PID = not is_control_by_PID
                    print("you have reached the destination")
                    # time.sleep(2)
                    # pioneer_mini.land()

                ch_2 = 1500 - int(dVrot_k * dangle)
                ch_4 = 1500 + int(dVx)
                ch_3 = 1430  # 1350
                # ch_3 = 1500
                color = [0, 255, 0]
                frame = cv2.circle(frame, (10, 10), 10, color, cv2.FILLED)

            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                pioneer_mini.land()
                break

            elif key == ord("5"):
                nearby_pixels -= 10
            elif key == ord("6"):
                nearby_pixels += 10
            elif key == ord("7"):
                edge -= 2
            elif key == ord("8"):
                edge += 2

            elif key == ord("1"):
                pioneer_mini.arm()
            elif key == ord("2"):
                pioneer_mini.disarm()
            elif key == ord("3"):
                time.sleep(2)
                pioneer_mini.arm()
                time.sleep(1)
                pioneer_mini.takeoff()
                time.sleep(2)
            elif key == ord("4"):
                time.sleep(2)
                pioneer_mini.land()
                time.sleep(2)
            elif key == ord("w"):
                ch_3 = min_v
            elif key == ord("s"):
                ch_3 = max_v
            elif key == ord("a"):
                ch_4 = min_v
            elif key == ord("d"):
                ch_4 = max_v
            elif key == ord("q"):
                ch_2 = 2000
            elif key == ord("e"):
                ch_2 = 1000
            elif key == ord("i"):
                ch_1 = 2000
            elif key == ord("k"):
                ch_1 = 1000
            elif key == ord("p"):
                is_control_by_PID = not is_control_by_PID

            # print("ch3, ch2", ch_3, ch_2)

            pioneer_mini.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )

            cv2.imshow('live from your pc :)', frame_after_thresh)
            cv2.imshow('without changes', frame)
    except Exception as e:
        print(e)
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini
