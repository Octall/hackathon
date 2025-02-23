import time
import importlib.util
import threading
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
    print("Real GPIO")
except (ImportError, RuntimeError):
    import FakeRPi.GPIO as GPIO
import sys, json

servo_1 = 11
servo_2 = 13


GPIO.setmode(GPIO.BOARD)

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


def main():

    input_data = sys.stdin.read()
    print(input_data)
    try:
        data = json.loads(input_data)

        result = f"Servo moved to angle: {data}"
        changeAngle(data, 0)
        changeAngle(data, 1)
    except Exception as e:
        result = f"Error: {str(e)}"

    print(result)

    sys.stdout.flush()



if __name__ == "__main__":
    main()