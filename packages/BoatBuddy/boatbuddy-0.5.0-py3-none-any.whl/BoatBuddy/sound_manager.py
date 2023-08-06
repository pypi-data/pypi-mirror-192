import os
from threading import Thread, Event

from playsound import playsound

from BoatBuddy import utils


class SoundManager:

    def __init__(self, options):
        self._options = options
        self._sound_buffer = []
        self._sound_thread = None
        self._exit_signal = Event()

        if self._options.sound_module:
            self._sound_thread = Thread(target=self._play_sound_loop)
            self._sound_thread.start()

    def play_sound_async(self, filename):
        if not self._options.sound_module:
            return
        self._sound_buffer.append(filename)

    def finalize(self):
        if not self._options.sound_module:
            return

        self._exit_signal.set()
        if self._sound_thread:
            self._sound_thread.join()

    def _play_sound_loop(self):
        while not self._exit_signal.is_set():
            if len(self._sound_buffer):
                self._play_sound(self._sound_buffer.pop(0))

    @staticmethod
    def _play_sound(filename):
        full_path = os.path.dirname(os.path.abspath(__file__)) + filename
        utils.get_logger().debug(f'Playing a sound with filename: {full_path}')
        playsound(full_path)
