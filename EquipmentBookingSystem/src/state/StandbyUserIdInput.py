#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.AccountLedger import AccountLedger
from db.AccountRecord import AccountRecord
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res
import config

class StandbyUserIdInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("社員証をかざしてください")
        Console.puts(">", end="")
        if config.is_debug_mode():
            self.__input = input.SunitizedString(
                input.UserInputReader()
            )
        else:
            self.__input = input.SunitizedString(
                input.RFIDReader()
            )

        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        rfid = self.__input.get_string()
        if (rfid != ""):
            record = UserProcedure().get_user_record_by(rfid=rfid)

            if record is None:
                cmn_res.user.data[AccountRecord.RFID] = rfid
                self.__get_next_state = state.AppendNewUser()
            else:
                cmn_res.user.data = record

                Console.puts(
                    "ようこそ、社員番号",
                    cmn_res.user.data[AccountRecord.EMPLOYEE_ID],
                    "の",
                    cmn_res.user.data[AccountRecord.LAST_NAME],
                    cmn_res.user.data[AccountRecord.FIRST_NAME],
                    "さん", "\n")

                self.__get_next_state = state.GotoNextAfterWaiting()
                self.__get_next_state.set_next_state(
                    state.StandbyUserProcedureInput())

        else:
            self.__get_next_state = state.StandbyUserIdInput()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
