import socket
import struct
import pyautogui
import irProcessing

X_RANGE = 430
Y_MIN = -290
Y_MAX = 194
HOST = "0.0.0.0"
PORT = 64444
SCREEN = pyautogui.size()


def move(x, y):
    pyautogui.moveTo((1-(x+512)/1024) * SCREEN.width, (y+512)/1024 * SCREEN.height)
    pass


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                pyautogui.FAILSAFE = False
                pyautogui.PAUSE = 0

                while True:
                    try:
                        data = conn.recv(64)
                        d = data.decode("ascii")
                        if d[:4] != 'init':
                            print(f"Bruh, transmission error: {d}")
                            continue
                        if d[0] == '.':
                            break
                        d = d[4:]
                        # print(d)
                        if d[0] != 'a':
                            coords = d.split(";")
                            # print(coords)
                            res = irProcessing.ir(int(coords[0]),
                                                  int(coords[1]),
                                                  int(coords[2]),
                                                  int(coords[3]),
                                                  int(coords[4]),
                                                  int(coords[5]),
                                                  int(coords[6]),
                                                  int(coords[7]),
                                                  int(coords[8]),
                                                  int(coords[9]),
                                                  int(coords[10]),
                                                  )
                            # print(res)
                            if res[3]:
                                move(res[4], res[5])
                            elif res[0]:
                                move(res[1], res[2])

                    except ValueError as e:
                        print(e)
                    except IndexError as e:
                        print(e)
                conn.close()
