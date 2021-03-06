#!/usr/bin/env python

import time
import state as state
import dev.display.Console as Console
import dev.input as input


class StateController():
    def __init__(self):
        self.__current = state.Init()
        self.__current.entry()
        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()
        state.CommonResource.prev_state = self.__current

    def step(self):
        self.__pressed_key.capture()

        # Execute current state.
        self.__current.do()

        if (self.__current.should_exit()):
            self.__current.exit()

            next_state = self.__current.get_next_state()

            state.CommonResource.prev_state = self.__current

            self.__current = next_state

            self.__current.entry()

            self.__restart_timer()

        elif not isinstance(self.__current, (state.Init, state.Restart)):
            if self.__timeout_detected() or self.__pressed_key.is_escape():
                state.CommonResource.prev_state = self.__current
                self.__current = state.Restart()
                self.__current.entry()
                self.__restart_timer()

    def run(self):
        while not isinstance(self.__current, state.Exit):
            time.sleep(0.010)
            self.step()

    def __restart_timer(self):
        self.__start_time = time.time()

    def __timeout_detected(self):
        # Refresh timer when any key pressed
        if self.__pressed_key.exists():
            self.__restart_timer()

        elapsed_time = time.time() - self.__start_time
        if (5 < elapsed_time):
            timeout_detected = True
            self.__restart_timer()

        else:
            timeout_detected = False

        return timeout_detected
