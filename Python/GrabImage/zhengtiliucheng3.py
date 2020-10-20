import Jetson.GPIO as GPIO
import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

# Pin Definitions:
#output pins
gpo1 = 37
gpo2 = 35
gpo3 = 33
gpo4 = 31
gpo5 = 29
gpo6 = 15
gpo7 = 13


#input pins
gpi_left_page = 32
gpi_grabimage = 36
gpi_right_page = 22


#reserved input pins
gpi_reserved_1 = 40
gpi_reserved_2 = 38



#reserved output pins
gpo_reserved_1 = 12
gpo_reserved_2 = 16
gpo_reserved_3 = 18


print_once_flag = 0
clickState = 0
firstTime = 0
secondTime = 0
program_step = 0
time_long_set = 0.5
time_long_long_set = 2
time_short_set = 0
timeEclipse = 0
clickFlag = 0
click_once =  0
falling_edge_flag = 0
rising_edge_flag = 0
cansel_flag = 0
ok_flag = 0




# blink LED 2 quickly 5 times when button pressed
def blink(channel):

    global clickState
    global firstTime
    global secondTime
    global program_step
    global print_once_flag
    global rising_edge_flag
    global falling_edge_flag
    global click_once

    #print("Blink LED 2, %s"%num)

    if(GPIO.input(channel)==GPIO.LOW):
        if(program_step == 0):
            falling_edge_flag = 1
            program_step = 1


        if(clickState == 0 and program_step == 2):
            firstTime = time.time()
            clickState = 1
            click_once = 1
            #print("state 1")
            
        if(clickState == 1 and click_once==0 and program_step == 2):
            secondTime = time.time()
            clickState = 2
            #print("state 2")
   
    elif(GPIO.input(channel)==GPIO.HIGH ):
        if(program_step == 1):
            rising_edge_flag = 1
            program_step = 2

           
    GPIO.remove_event_detect(channel)
    GPIO.add_event_detect(gpi_grabimage, GPIO.BOTH, callback=blink,bouncetime=200)







def main():

    global clickState
    global firstTime
    global secondTime
    global program_step
    global print_once_flag
    global timeEclipse
    global clickFlag
    global click_once
    global time_long_set
    global time_long_long_set
    global falling_edge_flag 
    global rising_edge_flag 
    global cansel_flag
    global ok_flag


    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    #GPIO.setup([led_pin_1, led_pin_2], GPIO.OUT)  # LED pins set as output
    GPIO.setup(gpi_grabimage, GPIO.IN)  # button pin set as input

    # Initial state for LEDs:
    #GPIO.output(led_pin_1, GPIO.LOW)
    #GPIO.output(led_pin_2, GPIO.LOW)

    GPIO.add_event_detect(gpi_grabimage, GPIO.BOTH, callback=blink, bouncetime=200)

   # print("Starting demo now! Press CTRL+C to exit")
    pwm = PCA9685()
    pwm.setPWMFreq(50)
    pwm.setPWM(3,0,0)#关闭可见激光 
    pwm.setPWM(4,0,0)#关闭红外光源 
    pwm.setPWM(5,0,0)#关闭红外激光 

    try:
        while True:
            
            if(clickState == 1):
                timeEclipse = time.time() - firstTime
                if(timeEclipse>time_long_set):
                    ok_flag = 1
                    clickFlag = 1
                    clickState = 0
                    firstTime = 0
                    #print("state 3")
                    
                else:
                    time.sleep(0.01)
                    click_once = 0
                

            if(clickState == 2):
                timeEclipse = secondTime-firstTime
                if(timeEclipse < time_long_set):
                    cansel_flag = 1
                    clickFlag = 2
                    secondTime = 0
                    firstTime = 0
                    clickState = 0





            if(clickFlag == 1 ):
                #print("this is single click")
                clickState = 0
                clickFlag=0
            elif(clickFlag == 2 ):
                #print("this is double click")
                clickState = 0
                clickFlag=0
            if(clickFlag == 3):
                clickState = 0
                clickFlag=0
                #print("this is changan")




            
            if(program_step == 1 and print_once_flag==0):
                #print("点亮可见激光")
                #print("点亮不可见激光")
                #print("点亮光源")
                pwm.setPWM(3,0,4095)#点亮可见激光 
                pwm.setPWM(4,0,4095)#点亮红外光源 
                pwm.setPWM(5,0,4095)#点亮红外激光
                print("======================================================================")
                print_once_flag=1
            if(program_step == 2 and print_once_flag==1):
                #print("熄灭光源")
                pwm.setPWM(4,0,0)#熄灭红外光源 
                print("抓拍一张激光图像")#将此句话替换成拍照激光图片的函数即可
                time.sleep(0.5)






                pwm.setPWM(3,0,0)#熄灭可见激光 
                pwm.setPWM(5,0,0)#熄灭红外激光
                print("抓拍一张heise图像")#将此句话替换成拍照heise图片的函数即可
                



                #print("打开光源")
                #print("熄灭可见激光")
                #print("熄灭不可见激光")
                pwm.setPWM(4,0,4095)#打开红外光源 
                pwm.setPWM(3,0,0)#熄灭可见激光 
                pwm.setPWM(5,0,0)#熄灭红外激光
                print("抓拍一张灰度图像")#将此句话替换成拍照灰度图片的函数即可
                time.sleep(0.5)
                pwm.setPWM(4,0,0)#熄灭红外光源 


                print("开始上传激光图像")#将此句话替换成上传激光图片的函数即可
                print("开始上传灰度图像")#将此句话替换成上传灰度图片的函数即可


                time.sleep(0.5)
                print("显示轮廓图像")#将此句话替换成显示轮廓图片的函数即可
                print("等待确认回复")
                print("======================================================================")
                print_once_flag =2
           
            if(program_step==2 and cansel_flag==1 and print_once_flag==2):
                cansel_flag=0
                print("取消重新开始")
                print("======================================================================")
                print_once_flag=0
                program_step=0

            if(program_step==2 and ok_flag==1 and print_once_flag==2):
                ok_flag =0
                print("确认重新开始")
                print("======================================================================")
                print_once_flag=0
                program_step=0

            
                
            





    finally:
        GPIO.cleanup()  # cleanup all GPIOs

if __name__ == '__main__':
    main()
