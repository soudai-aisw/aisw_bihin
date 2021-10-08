#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.AccountLedger import AccountLedger
from db.AccountRecord import AccountRecord
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res

class ConfirmToAppendNewUser(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("以下の情報で登録します。よろしいですか？(Y/N)")
        Console.puts("RFID      ：", cmn_res.user.data[AccountRecord.RFID])
        Console.puts("USER ID  ：", cmn_res.user.data[AccountRecord.EMPLOYEE_ID])
        Console.puts("LAST NAME  ：", cmn_res.user.data[AccountRecord.LAST_NAME])
        Console.puts("FIRST NAME  ：", cmn_res.user.data[AccountRecord.FIRST_NAME])

        Console.puts(">", end="")
        self.__input = input.SunitizedString(
            input.ConsoleTextField()
        )

        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        if (self.__input.get_string() in ["y","Y"]):
            Console.puts("ユーザ情報を登録しました。")
            AccountLedger(True).update(cmn_res.user)
        else:
            Console.puts("ユーザ情報を登録せずに戻ります。")
        self.__get_next_state = state.GotoNextAfterWaiting()
        self.__get_next_state.set_next_state(state.StandbyUserIdInput())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
