#!/usr/bin/env python

import time

import state as state
import dev.display.Console as Console
import dev.input as input


class Restart(state.IState):
    def entry(self):
        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()
        Console.clear()
        if state.CommonResource.employeeId != "":
            Console.puts(state.CommonResource.employeeId, "さん。")
        Console.puts("一定時間操作がなかったか終了コードを受け付けたためエントランスに戻ります。")

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        return state.Init()

    def should_exit(self):
        return self.__pressed_key.exists() or self.__timeout_detected()

    # 3秒経過でタイムアウト
    def __timeout_detected(self):
        elapsed_time = time.time() - self.__start_time
        return (3 < elapsed_time)
