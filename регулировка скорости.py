from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time
from median_trace import get_black_point

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

            xc, yc, _ = frame.shape

            ccol, crow = get_black_point(frame)

            dx = xc - ccol
            dy = yc - crow
            print("dx, dy", dx, dy)
            dV_max = 400
            dVx = dV_max * (dx / xc)
            dVy = dV_max * (dy / yc)

            print("dVx, dVy", dVx, dVy)

            if dx < 70:
                dx = 0
            else:
                ch_3 = 1500 + int(dVy)
                ch_4 = 1500 + int(dVx)


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


            # print("ch3, ch4", ch_3, ch_4)

            pioneer_mini.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )
            time.sleep(0.02)
    except Exception as e:
        print(e)
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini

