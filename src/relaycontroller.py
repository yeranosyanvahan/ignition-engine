import RPi.GPIO as GPIO

class RelayController:
    def __init__(self):
        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Define the GPIO pins for the relays
        self.relay_pins = {
            "podsos": 17,
            "onoff": 27,
            "starter": 22,
            "ongen": 24,
        }

        # Set the pins as OUTPUT
        GPIO.setup(list(self.relay_pins.values()), GPIO.OUT)

        # Set all relays to the "up" state (HIGH)
        for relay_pin in self.relay_pins.values():
            GPIO.output(relay_pin, GPIO.HIGH)

    def off(self, relay_name):
        if relay_name in self.relay_pins:
            GPIO.output(self.relay_pins[relay_name], GPIO.HIGH)
        else:
            print(f"Unknown relay: {relay_name}")

    def on(self, relay_name):
        if relay_name in self.relay_pins:
            GPIO.output(self.relay_pins[relay_name], GPIO.LOW)
        else:
            print(f"Unknown relay: {relay_name}")


    def __del__(self):
        self.cleanup()

    def cleanup(self):
        # Clean up and release the GPIO pins
        GPIO.cleanup()

# Example usage:
if __name__ == "__main__":
    relay_controller = RelayController()

    # Example: Turn on a relay
    relay_controller.on("relay1")
    relay_controller.on("relay3")
    relay_controller.on("relay4")

    # Wait for a few seconds (example delay)
    input("Press Enter to continue...")
    relay_controller.off("relay2")

    # Example: Turn off a relay
    relay_controller.off("relay1")

    # Clean up GPIO pins when done
    relay_controller.cleanup()
