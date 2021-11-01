#!/usr/bin/env python
from db.EquipmentRecord import EquipmentRecord
from db.EquipmentLedger import EquipmentLedger
import state as state
import dev.display.Console as Console
from state.commonResource import CommonResource as cmn_res
from db.UserProcedure import UserProcedure
from dev.input import input

class ConfirmToAppendNewEquipment(state.IState):
    def entry(self):
        self.__input = input.SunitizedString(
            input.ConsoleTextField()
        )
        self.__get_next_state = state.ErrorHasOccurred()

        Console.clear()
        Console.puts("以下の内容で手続きを行います。よろしいですか？(Y/N)")
        Console.puts("機材ID    ：", cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_ID])
        Console.puts("機材名    ：", cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_NAME])
        Console.puts("RFID：", cmn_res.equipment.data[EquipmentRecord.RFID])
        Console.puts(">", end="")
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        if( self.__input.get_string() in ["y","Y"]):
            Console.puts("RFIDとの関連付けが完了しました。")
            EquipmentLedger(True).update(cmn_res.equipment)
        else:
            Console.puts("関連付けをキャンセルしました。")

        self.__get_next_state = state.GotoNextAfterWaiting()
        self.__get_next_state.set_next_state(state.AppendNewEquipment())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
