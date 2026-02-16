import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
led = 26
u = 6
GPIO.setup(led, GPIO.OUT)
GPIO.setup(u, GPIO.IN)

while True:
    if GPIO.input(u):
        GPIO.output(led, not GPIO.input(u))
