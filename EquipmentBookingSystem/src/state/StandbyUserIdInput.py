#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.AccountLedger import AccountLedger
from db.AccountRecord import AccountRecord


class StandbyUserIdInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("社員証をかざしてください")
        Console.puts(">", end="")
        self.__input = input.SunitizedString(
            input.UserInputReader()
        )

        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        rfid = self.__input.get_string()
        print(rfid)
        if (rfid != ""):
            records = AccountLedger().find_by(AccountRecord.RFID, rfid)

            if len(records) == 0:
                Console.puts("存在しない社員番号です")
                Console.puts("再度試しても失敗する場合、システム管理者に問い合わせてください。")
                self.__get_next_state = state.ErrorHasOccurred()
            elif len(records) == 1:
                record = records.loc[0]
                Console.puts(
                    "ようこそ、社員番号",
                    record[AccountRecord.EMPLOYEE_ID],
                    "の",
                    record[AccountRecord.LAST_NAME],
                    record[AccountRecord.FIRST_NAME],
                    "さん", "\n")
                state.CommonResource.employeeId = \
                    record[AccountRecord.EMPLOYEE_ID]
                self.__get_next_state = state.GotoNextAfterWaiting()
                self.__get_next_state.set_next_state(
                    state.StandbyUserProcedureInput())
            else:
                raise SystemError("AccountLedger returned multiple records.")

        else:
            self.__get_next_state = state.StandbyUserIdInput()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
