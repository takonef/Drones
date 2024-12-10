from pioneer_sdk import Pioneer, Camera
import cv2
import numpy as np
import time

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
    frame_rate = 1
    try:
        while True:
            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000
            frame = camera.get_frame()
            thresh = 100
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
            a = np.array(bw_frame)
            a_size = a.shape
        
            if frame is not None:
                camera_frame = cv2.imdecode(
                    np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
                )
                key = cv2.waitKey(1)
                if key == ord("u"):
                    while True:
                        frame = camera.get_frame()
                        time_previous = 0
                        time_passed = time.time() - time_previous
                        if time_passed > (1 / frame_rate):  # т.е. мы хотим frame_rate кадров в секунду, тогда кадр появляется каждые 1/frame_rate секунды (получается перед показом каждого следующего кадра, мы проверяем, прошло ли 1/frame_rate секунд с показа предыдущего кадра)
                            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            thresh = 100
                            bw_frame = cv2.threshold(gray_frame, thresh, 255, cv2.THRESH_BINARY)[1]
                            time_previous = time.time()
                            a = np.array(bw_frame)
    
                            sum_rows = np.sum(a, axis=1)
                            sum = 0
                            am = 0
                            for i in range(rows):
                                if (255 * columns - sum_rows[i]) != 0:
                                    sum += i
                                    am += 1
                            if am != 0:
                                crow = sum // am
                            else:
                                crow = 0
                                print("Bah")
    
                            sum_columns = np.sum(a, axis=0)
                            sum = 0
                            am = 0
                            for i in range(columns):
                                if (255 * rows - sum_columns[i]) != 0:
                                    sum += i
                                    am += 1
                            if am != 0:
                                ccol = sum // am
                            else:
                                ccol = 0
                                print("Bah")
                            bw_frame[crow][ccol] = 255
                            print(crow, ccol)  # ряд(высота - у) и колонна(сторона - х)
    
                            xc = columns / 2
                            yc = rows / 2
    
                            dx = xc - ccol
                            dy = yc - crow
                            dV_max = 400 #можно менять
                            dVx = dV_max * (dx / xc)
                            dVy = dV_max * (dy / yc)
    
                            if dx < 70: #можно менять
                                dx = 0
                            else:
                                ch_3 = 1500 + dVy
                                ch_4 = 1500 + dVx
    
                        cv2.imshow('live from your drone:)', bw_frame)
                        if cv2.waitKey(1) == ord('q'):
                            break

                bw_frame.release()
                cv2.destroyAllWindows()

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

