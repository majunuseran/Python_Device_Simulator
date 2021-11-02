import config as constants
import uuid
import time
import json
import asyncio
import RPi.GPIO as GPIO
from ConfigEditor import ConfigEditor

async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(int(constants.LIGHT_OUT_GPIO_PIN_ADDRESS), GPIO.OUT)
    GPIO.setup(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.OUT)
    GPIO.setup(constants.SWITCH_IN_GPIO_PIN_ADDRESS, GPIO.IN)
    GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, False)
    GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.HIGH)
    time.sleep(15)
    GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.LOW)


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

