#!/usr/bin/env python

from db.AccountRecord import AccountRecord
from db.EquipmentRecord import EquipmentRecord
import time

import state as state
import dev.display.Console as Console
import dev.input as input
import config
from state.commonResource import CommonResource as cmn_res

class Restart(state.IState):
    def entry(self):
        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()
        Console.clear()
        Console.puts("一定時間操作がなかったか終了コードを受け付けたためエントランスに戻ります。")

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        return state.Init()

    def should_exit(self):
        return self.__pressed_key.exists() or self.__timeout_detected()

    def __timeout_detected(self):
        elapsed_time = time.time() - self.__start_time
        return (config.get_time_of_message_display() < elapsed_time)
