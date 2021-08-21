#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import config


class SuccessReturnEquipment(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("ユーザID  ：", state.CommonResource.employeeId)
        Console.puts("機材ID    ：", state.CommonResource.equipmentId, "\n")
        Console.puts("上記の情報で備品の返却手続きが完了しました。\n")
        Console.puts("続けて他の機器の返却処理が実施できます。")
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        pass

    def exit(self):
        self.__get_next_state = state.GotoNextAfterWaiting()
        # 連続で貸出処理を行うためID入力へ遷移
        self.__get_next_state.set_next_state(
            state.StandbyReturnEquipmentIdRead())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return True
