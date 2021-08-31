#!/usr/bin/env python

import state
import time

import dev.display.Console as Console
import dev.input as input
import config
from state.commonResource import CommonResource as cmn_res

class ErrorHasOccurred(state.IState):
    def entry(self):
        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        return cmn_res.prev_state

    def should_exit(self):
        return self.__pressed_key.exists() or self.__timeout_detected()

    # 3秒経過でタイムアウト
    def __timeout_detected(self):
        elapsed_time = time.time() - self.__start_time
        return (config.get_time_of_error_display() < elapsed_time)
