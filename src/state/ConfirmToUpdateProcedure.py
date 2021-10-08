#!/usr/bin/env python
from db.EquipmentRecord import EquipmentRecord
from db.AccountRecord import AccountRecord
import state as state
import dev.display.Console as Console
from state.commonResource import CommonResource as cmn_res
from db.UserProcedure import UserProcedure
from dev.input import input

class ConfirmToUpdateProcedure(state.IState):
    def entry(self):
        self.__input = input.SunitizedString(
            input.ConsoleTextField()
        )
        self.__get_next_state = state.ErrorHasOccurred()

        Console.clear()
        Console.puts("以下の内容で手続きを行います。よろしいですか？(Y/N)")
        Console.puts("ユーザID  ：", cmn_res.user.data[AccountRecord.EMPLOYEE_ID])
        Console.puts("機材ID    ：", cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_ID])
        Console.puts("機材名    ：", cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_NAME])
        Console.puts("返却予定日：", cmn_res.equipment.data[EquipmentRecord.END_DATE])
        Console.puts(">", end="")
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        if( self.__input.get_string() in ["y","Y"]):
            result = UserProcedure(True).update_equipment_return_date(
                cmn_res.user.data[AccountRecord.EMPLOYEE_ID],
                cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_ID],
                cmn_res.equipment.data[EquipmentRecord.END_DATE])
            if result == True:
                self.__get_next_state = state.SuccessUpdateEquipment()
            else:
                Console.puts("更新の受理に失敗しました。")
                Console.puts("再度試しても失敗する場合、システム管理者に問い合わせてください。", "\n")
                self.__get_next_state = state.ErrorHasOccurred()
        else:
            Console.puts("更新手続きをキャンセルしました。")
            self.__get_next_state = state.GotoNextAfterWaiting()
            self.__get_next_state.set_next_state(state.StandbyUpdateEquipmentIdInput())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
