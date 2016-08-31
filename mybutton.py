import mraa
import time

button = mraa.Gpio(60)
button.dir(mraa.DIR_IN)

def is_press_3s():
    if (button.read()):
        time.sleep(0.5)
        if (button.read()):
            print("button press")
            return True
        else:
            return False
    else:
        return False



if __name__ == '__main__':
    while True:
        is_press_3s()
        time.sleep(1)
        
        
