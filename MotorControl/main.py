import time
import importlib.util
import threading
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
    print("Real GPIO")
except (ImportError, RuntimeError):
    import FakeRPi.GPIO as GPIO


servo_1 = 11
servo_2 = 13

GPIO.setmode(GPIO.BOARD)

print("success?")

GPIO.setup(servo_1, GPIO.OUT)
GPIO.setup(servo_2, GPIO.OUT)

pwm = [GPIO.PWM(servo_1, 50), GPIO.PWM(servo_2, 50)]

for i in pwm:
    i.start(0)

def changeAngle(angle, servo):
    duty_cycle = 2.5 + (angle / 180.0) * 10  # Maps 0-180° to 2.5-12.5%
    pwm[servo].ChangeDutyCycle(duty_cycle)
    print(angle)
    time.sleep(0.5)  # allow the servo time to reach the position
    pwm[servo].ChangeDutyCycle(0)  # stop sending signals to hold the position




thread1 = threading.Thread(target=changeAngle(180,1))
thread2 = threading.Thread(target=changeAngle(180,0))

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()

thread1.join()
thread2.join()

time.sleep(2)

changeAngle(180, 1)
changeAngle(135,0)

time.sleep(2)

changeAngle(0, 1)
changeAngle(0, 0)

time.sleep(2)

changeAngle(180,1)
changeAngle(180,0)

time.sleep(2)

changeAngle(0, 1)
changeAngle(0, 0)
