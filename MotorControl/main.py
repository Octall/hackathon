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


def process_command(data):
    try:
        # Assuming the data is a JSON object containing an 'angle'
        # Process the angle here (e.g., control your servo)
        changeAngle(data.get("yaw"), 0)
        changeAngle(data.get("pitch"), 1)
        result = f"Servo moved to angle: {data}"
    except Exception as e:
        result = f"Error: {str(e)}"
    return result

def main():
    while True:
        # Read one line at a time from stdin
        line = sys.stdin.readline()
        if not line:
            # If readline returns an empty string, no more data is coming.
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {str(e)}")
            sys.stdout.flush()
            continue
        
        # Process the command
        result = process_command(data)
        print(result)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
