from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time
# from line_trace_top_bottom import *
from line_only_top import *

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
    pioneer_mini = Pioneer()
    camera = Camera()
    min_v = 1300
    max_v = 1700
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


            # print("xc, yx", xc, yc)


            frame_after_thresh, dx = get_black_line(frame)

            # print("ccol, crow", ccol, crow)


            dV_max = 300
            dVx = dV_max * (dx / xc)
            

            limit = 300
            if dVx > limit:
                dVx = limit
                print("bah")
            if dVx < -limit:
                dVx = -limit
                print("bah")

            

            # print("dVx, dVy", dVx, dVy)

            if not is_control_by_PID:
                dx = 0
            else:
                ch_2 = 1500 + int(dVx)
                ch_3 = 1350



            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                pioneer_mini.land()
                break
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

            print("ch3, ch2", ch_3, ch_2)


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
