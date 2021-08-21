#!/usr/bin/env python

import time
import state as state
import dev.display.Console as Console
import dev.input as input
import db.Registration.DBregistration as dbregist


class StandbyExpirationDateInputWhenBarrow(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("返却予定日を入力してください(yyyy/mm/dd)")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        return_date = self.__input.get_string()
        # この間に返却日の内容が正しいかチェックを実施する処理を入れる（レベルアップ）
        result = dbregist.DBregistration_Borrow(
            state.CommonResource.equipmentId, state.CommonResource.employeeId, return_date)
        if result == True:
            Console.puts("返却予定日", return_date, "を受理しました")
            state.CommonResource.expirationDate = return_date
            self.__get_next_state = state.GotoNextAfterWaiting()
            self.__get_next_state.set_next_state(
                state.SuccessBarrowEquipment())
        else:
            Console.puts("借用の受理に失敗しました。")
            Console.puts("再度試しても失敗する場合、システム管理者に問い合わせてください。", "\n")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
