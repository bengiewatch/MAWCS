import smbus
import math
import time
import RPi.GPIO as GPIO
 
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
servo = 22
servo2 = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)
p=GPIO.PWM(servo,50)
q=GPIO.PWM(servo2,50)
currentvalue = 2.5
currentvalue2 = 2.5
p.start(2.5)
q.start(2.5)
 
 
def read_byte(adr):
    return bus.read_byte_data(address, adr)
 
 
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val
 
 
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
 
def dist(a, b):
    return math.sqrt((a * a) + (b * b))
 
 
def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)
 
 
def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)
 
 
bus = smbus.SMBus(1)
address = 0x68
 
bus.write_byte_data(address, power_mgmt_1, 0)
 
while True:
    print ("Gyroscope data")
    #print "--------------"
 
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
 
    print ("{}\t{}\t{}\t{}".format ("X out: ", gyro_xout, "scaled: ", (gyro_xout/131)))
    print ("{}\t{}\t{}\t{}".format ("Y out: ", gyro_yout, " scaled: ", (gyro_yout / 131)))
    print ("{}\t{}\t{}\t{}".format ("Z out: ", gyro_zout, " scaled: ", (gyro_zout / 131)))
    time.sleep(2)
 
#     print
#     print "Accelerometer data"
#     print "------------------"
 
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
 
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
 
    #print "{}\t{}\t{}\t{}".format ("X out: ", accel_xout, " scaled: ", accel_xout_scaled)
    #print "{}\t{}\t{}\t{}".format ("Y out: ", accel_yout, " scaled: ", accel_yout_scaled)
    #print "{}\t{}\t{}\t{}".format ("Z out: ", accel_zout, " scaled: ", accel_zout_scaled)
     
    #print
 
    #print "X rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    #print "Y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
     
    #print
 
    time.sleep(1)
    AcX=accel_xout
    AcY=accel_yout

    if(AcX<-6000):
        print("forward")
        print("duty cycle:" + str(currentvalue))
        if(currentvalue<=10):
            p.ChangeDutyCycle(currentvalue+1)
            currentvalue+=1

        else:
            continue

    elif(AcX>6000):
        print("back")
        print("duty cycle:" +str(currentvalue))
        if(currentvalue>=1):
            p.ChangeDutyCycle(currentvalue-1)
            currentvalue-=1

        else:
            continue
            
            

    elif(AcY<-6000 ):
        print("left")
        print("duty cycle: "+str(currentvalue2))
        if(currentvalue2>=1):
            q.ChangeDutyCycle(currentvalue2+1)
            currentvalue2-=1

        else:
            continue
    
    elif(AcY>6000):
        print("right")
        print("duty cycle: "+str(currentvalue2))
        if(currentvalue2<=10):
            p.ChangeDutyCycle(currentvalue2+1)
            currentvalue2+=1

        else:
            continue

    elif(AcX<6000 and AcX>-6000 and AcX<6000 and AcX>-6000 ):
        print("stop")
        print("Current Duty Cycles of Servo motors")
        print(currentvalue)
        print(currentvalue2)
    else:
        print("nothing")
`