import RPi.GPIO as GPIO

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin you want to set to low
gpio_pin = 17

# Set the GPIO pin to a low state
GPIO.setup(gpio_pin, GPIO.OUT)
GPIO.output(gpio_pin, GPIO.LOW)

# Cleanup when done
GPIO.cleanup()