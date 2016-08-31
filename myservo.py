#coding=utf-8
import time
import pyupm_servo as servo

s = servo.ES08A(13)

def turn():
    for i in range(45,165):
        s.setAngle(i)
        time.sleep(0.015)

if __name__ == '__main__':
    while True:
        turn()
        time.sleep(1)