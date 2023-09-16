import RPi.GPIO as GPIO

class RelayController:
    def __init__(self):
        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Define the GPIO pins for the relays
        self.relay_pins = {
            "relay1": 17,
            "relay2": 27,
            "relay3": 22,
            "relay4": 24,
        }

        # Set the pins as OUTPUT
        GPIO.setup(list(self.relay_pins.values()), GPIO.OUT)

        # Set all relays to the "up" state (HIGH)
        for relay_pin in self.relay_pins.values():
            GPIO.output(relay_pin, GPIO.HIGH)

    def up(self, relay_name):
        if relay_name in self.relay_pins:
            GPIO.output(self.relay_pins[relay_name], GPIO.HIGH)
        else:
            print(f"Unknown relay: {relay_name}")

    def down(self, relay_name):
        if relay_name in self.relay_pins:
            GPIO.output(self.relay_pins[relay_name], GPIO.LOW)
        else:
            print(f"Unknown relay: {relay_name}")

    def cleanup(self):
        # Clean up and release the GPIO pins
        GPIO.cleanup()

# Example usage:
if __name__ == "__main__":
    relay_controller = RelayController()

    # Example: Turn on a relay
    relay_controller.down("relay1")

    # Wait for a few seconds (example delay)
    input("Press Enter to continue...")

    # Example: Turn off a relay
    relay_controller.up("relay1")

    # Clean up GPIO pins when done
    relay_controller.cleanup()
