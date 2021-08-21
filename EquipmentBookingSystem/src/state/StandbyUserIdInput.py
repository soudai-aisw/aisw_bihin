#!/usr/bin/env python


import time
import state as state
import dev.display.Console as Console
import dev.input as input
import db.matching.DBmatching as db


class StandbyUserIdInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("社員証をかざしてください")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        employee_id = self.__input.get_string()
        if (employee_id != ""):
            match_id = db.DBmatching_EmpIDtoEmpNo(employee_id)

            # False以外=登録済みユーザー
            if (match_id != False):
                # ここに社員名をDBから取得して表示したい（レベルアップ）
              #  name = db.名前取得(match_id)
                Console.puts("ようこそ", match_id, "さん", "\n")
                state.CommonResource.employeeId = match_id
                self.__get_next_state = state.GotoNextAfterWaiting()
                self.__get_next_state.set_next_state(
                    state.StandbyUserProcedureInput())
            else:
                Console.puts("存在しない社員番号です")
                Console.puts("再度試しても失敗する場合、システム管理者に問い合わせてください。")
                self.__get_next_state = state.ErrorHasOccurred()

        else:
            self.__get_next_state = state.StandbyUserIdInput()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
