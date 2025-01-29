import threading
import time
import traceback

from pioneer_sdk import Pioneer

from aruco_detect import *
from camera_pio import *
from line_only_top import fight_follow_line, change_near_by_pixels, change_edge


def camera_start():
    global global_frame
    while True:
        global_frame = get_cv_frame()


global_frame = None


def main():
    global global_frame
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

    min_v_manual_wasd_control = 1300
    max_v_manual_wasd_control = 1700

    th1 = threading.Thread(target=camera_start)
    th1.start()

    status = 0  # 0 -- до взлёта, 1 -- до включения режима автономного пилотирования, 2 -- стабилизация над маркером старта, 3 -- полёт по линии, 4 -- найден маркер финиша в центре изображения, посадка на него, 5 -- закончилась чёрная линия во время полёта

    try:
        while True:
            if global_frame is None:
                continue

            frame = np.array(global_frame)

            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000

            frame_center_y, frame_center_x, _ = map(lambda x: x // 2 - 1, frame.shape)

            status_circle_color = (0, 0, 255)
            start_marker_id = 0
            finish_marker_id = 1

            min_drone_flight_height = 0.2

            # TODO вынести предобработку картинки с выделенной линей в отдельную функцию
            frame_after_thresh, _, _, _, _ = fight_follow_line(global_frame, frame_center_x)

            match status:
                case 2:
                    status_circle_color = (0, 255, 255)
                    frame, ch_3, ch_4 = stabilize_at_marker(frame, frame_center_x, frame_center_y)
                    if is_marker_in_center_area(frame, start_marker_id, frame_center_x, frame_center_y):
                        status = 3
                case 4:
                    status_circle_color = (0, 255, 255)
                    frame, ch_3, ch_4 = stabilize_at_marker(frame, frame_center_x, frame_center_y)
                    ch_1 = 1400  # вниз
                    if pioneer_mini.get_dist_sensor_data(get_last_received=True) < min_drone_flight_height:
                        pioneer_mini.land()
                        time.sleep(1)
                        pioneer_mini.disarm()
                case 3:
                    status_circle_color = (0, 255, 0)
                    frame_after_thresh, status, ch_2, ch_3, ch_4 = fight_follow_line(global_frame, frame_center_x)
                    if is_marker_in_center_area(frame, finish_marker_id, frame_center_x, frame_center_y):
                        status = 4

            cv2.circle(frame, (10, 10), 10, status_circle_color, cv2.FILLED)  # отрисовка статуса

            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                pioneer_mini.land()
                break
            elif key == ord("5"):
                change_near_by_pixels(-1)
            elif key == ord("6"):
                change_near_by_pixels(1)
            elif key == ord("7"):
                change_edge(-1)
            elif key == ord("8"):
                change_edge(1)
            elif key == ord("1"):
                pioneer_mini.arm()
            elif key == ord("2"):
                pioneer_mini.disarm()
            elif key == ord("3"):
                status = 1
                time.sleep(2)
                pioneer_mini.arm()
                time.sleep(1)
                pioneer_mini.takeoff()
                time.sleep(2)
            elif key == ord("4"):
                pioneer_mini.land()
                time.sleep(2)
            elif key == ord("w"):
                ch_3 = min_v_manual_wasd_control
            elif key == ord("s"):
                ch_3 = max_v_manual_wasd_control
            elif key == ord("a"):
                ch_4 = min_v_manual_wasd_control
            elif key == ord("d"):
                ch_4 = max_v_manual_wasd_control
            elif key == ord("q"):
                ch_2 = 2000
            elif key == ord("e"):
                ch_2 = 1000
            elif key == ord("i"):
                ch_1 = 2000
            elif key == ord("k"):
                ch_1 = 1000
            elif key == ord("p"):
                if status == 5:
                    status = 3
                elif status == 1:
                    status = 2
                else:
                    status = 1  # выход из режима пилотирования

            print(status, ch_1, ch_2, ch_3, ch_4)

            pioneer_mini.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )

            cv2.imshow('line view', frame_after_thresh)
            cv2.imshow('original image', frame)
    except Exception:
        print(traceback.format_exc())
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini


if __name__ == '__main__':
    main()
