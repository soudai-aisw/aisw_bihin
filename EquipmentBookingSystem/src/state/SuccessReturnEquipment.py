#!/usr/bin/env python

import time
import state as state
import dev.display.Console as Console
import dev.input as input
import config


class SuccessReturnEquipment(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("ユーザID  ：", state.CommonResource.employeeId)
        Console.puts("機材ID    ：", state.CommonResource.equipmentId, "\n")
        Console.puts("上記の情報で備品の返却手続きが完了しました。")
        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        Console.clear()
        Console.puts("続けて他の機器の返却処理が実施できます。")
        return state.StandbyReturnEquipmentIdRead()

    def should_exit(self):
        return self.__pressed_key.exists() or self.__timeout_detected()

    def __timeout_detected(self):
        elapsed_time = time.time() - self.__start_time
        return (config.get_time_of_message_display() < elapsed_time)
