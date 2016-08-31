#coding=utf-8
import myoled 
import myfinger
import myservo
import mybutton
import mypir
import time


if __name__ == "__main__":
    while True: 
        if (mybutton.is_press_3s()):
            with open("mydata","r+b") as mydata:
                fingernum = int(mydata.readline()) + 1
                if(myfinger.store_finger(fingernum)== "SUCCESS"):
                    mydata.seek(0)
                    mydata.write(str(fingernum))
                    print(fingernum)
                    myoled.clear()
                    time.sleep(2)
        
        myoled.show_static()
        
        if (mypir.detect_people()):           
            fID = myfinger.check_finger()
            if (fID != "ERROR" and fID !="NoThisFinger"):
                print ("No: %d" % fID)
                myservo.turn()
                time.sleep(1)
                
        time.sleep(0.5)        
    

