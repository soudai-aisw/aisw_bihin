#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.AccountLedger import AccountLedger
from db.AccountRecord import AccountRecord
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res
import math

class AppendNewUser(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("登録されていないRFIDです。社員番号を入力してください")
        Console.puts(">", end="")
        self.__input = input.SunitizedString(
            input.UserInputReader()
        )

        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        employee_id = self.__input.get_string()
        if (employee_id != ""):
            record = UserProcedure().get_user_record_by(employee_id=employee_id)

            if record is None:
                Console.puts("存在しない社員番号です")
                Console.puts("システム管理者に問い合わせてください")
                self.__get_next_state = state.ErrorHasOccurred()
                return
            
            rfid = record[AccountRecord.RFID]
            if type(rfid) is float:
                if math.isnan(record[AccountRecord.RFID]):
                    rfid = ""

            if rfid=="":
                rfid = cmn_res.user.data[AccountRecord.RFID]
                cmn_res.user.data = record
                cmn_res.user.data[AccountRecord.RFID] = rfid
                self.__get_next_state = state.ConfirmToAppendNewUser()
            else:
                Console.puts("社員番号",employee_id,"には既にRFID",record[AccountRecord.RFID],"が関連付けられています")
                Console.puts("システム管理者に問い合わせてください")
                self.__get_next_state = state.ErrorHasOccurred()

        else:
            self.__get_next_state = state.AppendNewUser()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
