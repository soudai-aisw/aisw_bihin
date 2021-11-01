#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.UserProcedure import UserProcedure
from db.EquipmentRecord import EquipmentRecord
from state.commonResource import CommonResource as cmn_res

class AppendNewEquipment(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("関連付ける機材IDをキーボードで入力してください")
        Console.puts(">", end="")
        self.__input = input.SunitizedString(
            input.ConsoleTextField()
        )
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        # キーボード入力受付（Enterが押されたらexitへ移行する）
        self.__input.capture()

    def exit(self):
        # キーボード情報取得
        equipment_id = self.__input.get_string()

        if(equipment_id != ""):
            record = UserProcedure().get_equipment_record_by(equipment_id=equipment_id)

            if record is None:
            # IDがDB上登録されていない場合
                Console.puts("登録されていない備品です。", "\n")
                Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
                self.__get_next_state = state.ErrorHasOccurred()
            else:
                cmn_res.equipment.data = record
                if (cmn_res.equipment.data[EquipmentRecord.RFID] != "0"):
                    Console.puts(equipment_id,"は既にRFID:",cmn_res.equipment.data[EquipmentRecord.RFID],"が関連付けられています。", "\n")
                    Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
                    self.__get_next_state = state.ErrorHasOccurred()
                else:
                    #登録処理へ
                    self.__get_next_state = state.StandbyAppendEquipmentIdRead()


    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
