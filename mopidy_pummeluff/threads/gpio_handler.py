'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

__all__ = (
    'GPIOHandler',
)

from logging import getLogger
from threading import Thread
from time import time

from RPi import GPIO  # pylint: disable=import-error

from mopidy_pummeluff import actions
from mopidy_pummeluff.sound import play_sound

LOGGER = getLogger(__name__)


class GPIOHandler(Thread):
    '''
    Thread which handles the GPIO ports, which basically means activating the
    LED when it's started and then reacting to button presses.
    '''

    def __init__(self, core, config, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param configparser.ConfigParser config: The config parser instance
        :param threading.Event stop_event: The stop event
        '''
        super().__init__()

        self.core       = core
        self.config     = config
        self.stop_event = stop_event

        self.init_pin_config()

    def init_pin_config(self):
        '''
        Initialise the GPIO pin config.
        '''
        config = self.config['pummeluff']
        names  = [name for name in config if name.endswith('_pin') and name != 'led_pin']
        now    = time()

        self.led_pin = config['led_pin']

        self.button_pins = {
            config[name]: {
                'action': getattr(actions, name[0:-4].replace('_', ' ').title().replace(' ', '')),
                'triggered': now,
            }
            for name in names
        }

    # pylint: disable=no-member
    def run(self):
        '''
        Run the thread.
        '''
        GPIO.setmode(GPIO.BOARD)

        for pin in self.button_pins:
            LOGGER.debug('Setup pin %s as button pin', pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda pin: self.button_push(pin))  # pylint: disable=unnecessary-lambda

        LOGGER.debug('Setup pin %s as LED pin', self.led_pin)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)

        self.stop_event.wait()
        GPIO.cleanup()  # pylint: disable=no-member

    def button_push(self, pin):
        '''
        Callback method when a button is pushed.

        :param int pin: Pin number
        '''
        now    = time()
        before = self.button_pins[pin]['triggered']

        if (GPIO.input(pin) == GPIO.LOW) and (now - before > 0.25):
            LOGGER.debug('Button at pin %s was pushed', pin)
            play_sound('success.wav')
            self.button_pins[pin]['action'].execute(self.core)
            self.button_pins[pin]['timestamp'] = now
