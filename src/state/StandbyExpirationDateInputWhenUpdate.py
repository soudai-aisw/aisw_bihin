#!/usr/bin/env python

from db.AccountRecord import AccountRecord
import time
import state as state
import dev.display.Console as Console
import dev.input as input
import cmn.ExpirationDateCheck as edchk
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res
from db.EquipmentRecord import EquipmentRecord


class StandbyExpirationDateInputWhenUpdate(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("返却予定日を入力してください", "(yyyy/mm/dd)")
        Console.puts(">", end="")
        self.__input = input.DateFormatedString(
            input.SunitizedString(
                input.ConsoleTextField()
            )
        )
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        return_date = self.__input.get_string()
        # 返却日の内容が正しいかチェック
        checkresult = edchk.ExpirationDateCheck(return_date, 90)
        if checkresult == True:
            cmn_res.equipment.data = {
                EquipmentRecord.END_DATE: return_date
            }
            self.__get_next_state = state.ConfirmToUpdateProcedure()
        else:
            Console.puts("返却予定日は今日を含めた90日以内を指定してください。")
            self.__get_next_state = state.GotoNextAfterWaiting()
            self.__get_next_state.set_next_state(
                state.StandbyExpirationDateInputWhenUpdate())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
