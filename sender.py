import socket
import time
from pyIRcam import pyIRcam
from pyMPU6050 import pyMPU6050

HOST = "192.168.100.100"
PORT = 64444
UPDATE_RATE = 0.10

if __name__ == '__main__':
    camera = pyIRcam()  # Sensor initialization
    gyro = pyMPU6050()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        while True:
            try:
                current = time.time()  # Counters for loop
                msg = 'init'.encode('ascii')
                elapsed = 0

                camera.getPositions()  # Update found IR objects
                gyro.getAccel()

                if camera.positions['found']:  # If an IR object is found, print the information
                    msg += f"{camera.positions['1'][0]:04d};" \
                           f"{camera.positions['1'][1]:04d};" \
                           f"{camera.positions['2'][0]:04d};" \
                           f"{camera.positions['2'][1]:04d};" \
                           f"{camera.positions['3'][0]:04d};" \
                           f"{camera.positions['3'][1]:04d};" \
                           f"{camera.positions['4'][0]:04d};" \
                           f"{camera.positions['4'][1]:04d};".encode("ascii")
                else:
                    msg += "abcd;efgh;hijk;lmno;pqrs;tuvw;xyz_;.!();".encode("ascii")
                msg += f"{gyro.accerelations[0]:06d};" \
                       f"{gyro.accerelations[1]:06d};" \
                       f"{gyro.accerelations[2]:06d}".encode("ascii")

                if len(msg) != 64:
                    raise Exception(f'Bad Msg: {msg}')
                s.send(msg)

                while elapsed < UPDATE_RATE:
                    elapsed = time.time() - current  # Wait until the loop completes, perfect update_rate loop
            except KeyboardInterrupt:
                print("Shutdown requested...exiting")
                break
            except Exception as e:
                print(e)
                break

        s.send('.'.encode("ascii"))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
