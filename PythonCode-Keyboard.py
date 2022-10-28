import time
import serial

ser = serial.Serial('COM8',9600)

def rc_control():
    user_input = input("Enter the direction :")
    if user_input == "8":# forward
        ser.write(b'8')
        rc_control()
    elif user_input == "5":# stop
        ser.write(b'5')
        rc_control()
    elif user_input == "2":# backward
        ser.write(b'2')
        rc_control()
    elif user_input == "6":# right
        ser.write(b'6')
        rc_control()
    elif user_input == "4":# left
        ser.write(b'4')
        rc_control()
    elif user_input == "quit" or user_input == "q":# exiting the program
        print("Program Exiting")
        time.sleep(0.1)
        ser.write(b'5')
        ser.close()
    else:
        print("Invalid input.Type\n'8' forward\n'5' stop\n'2' backward\n'6' right\n'4' left\n'quit or q' exit the program")
        rc_control()

time.sleep(2) # wait for the serial connection to initialize

rc_control()
