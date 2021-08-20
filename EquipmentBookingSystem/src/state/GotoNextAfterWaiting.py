#!/usr/bin/env python

import time

import state as state
import dev.display.Console as Console
import dev.input as input


class GotoNextAfterWaiting(state.IState):
    def entry(self):
        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def set_next_state(self, state):
        self.__next_state = state

    def get_next_state(self):
        return self.__next_state

    def should_exit(self):
        return self.__pressed_key.exists() or self.__timeout_detected()

    # 3秒経過でタイムアウト
    def __timeout_detected(self):
        elapsed_time = time.time() - self.__start_time
        return ( 1.5 < elapsed_time)
