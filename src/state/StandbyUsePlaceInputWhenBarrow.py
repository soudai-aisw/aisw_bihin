#!/usr/bin/env python

from re import T
from db.AccountRecord import AccountRecord
from db.EquipmentRecord import EquipmentRecord
import time
import state as state
import dev.display.Console as Console
import dev.input as input
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res
from cmn.UsePlace import UsePlace

class StandbyUsePlaceInputWhenBarrow(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("使用場所を入力して下さい。","{}:社内 {}:社外 {}:委託".format(
            UsePlace.InAISW, UsePlace.OutAISW, UsePlace.Outsourcer))
        Console.puts(">", end="")
        self.__input = input.SunitizedString(
            input.ConsoleTextField()
        )
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        use_place = self.__input.get_string()
        # 返却日の内容が正しいかチェック
        checkresult = UsePlace.Check(use_place)
        if checkresult == True:

            result = UserProcedure(True).borrow_equipment(
                cmn_res.user.data[AccountRecord.EMPLOYEE_ID],
                cmn_res.equipment.data[EquipmentRecord.RFID],
                cmn_res.equipment.data[EquipmentRecord.END_DATE],
                use_place + "X" )

            if result == True:
                place_name = UsePlace.ReturnName(use_place)
                Console.puts("使用場所", place_name, "を受理しました")
                cmn_res.equipment.data = {
                    EquipmentRecord.USE_PLACE: use_place
                }

                self.__get_next_state = state.GotoNextAfterWaiting()
                self.__get_next_state.set_next_state(
                    state.SuccessBarrowEquipment())

            else:
                Console.puts("借用の受理に失敗しました。")
                Console.puts("再度試しても失敗する場合、システム管理者に問い合わせてください。", "\n")
                self.__get_next_state = state.ErrorHasOccurred()
        else:
            Console.puts("使用場所を正しく入力してください。")
            self.__get_next_state = state.GotoNextAfterWaiting()
            self.__get_next_state.set_next_state(
                state.StandbyUsePlaceInputWhenBarrow())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
