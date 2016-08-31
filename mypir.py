import mraa
import time

pir = mraa.Aio(0)

def detect_people():
    if (pir.read()):
        print "someone is nearby!"
        return True
    else:
        return False
        
if __name__ == '__main__':
    while True:
        time.sleep(2)
        detect_people()
