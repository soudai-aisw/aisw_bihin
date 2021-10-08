#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res

class StandbyUpdateEquipmentIdInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("更新する機材のIDをキーボードで入力してください")
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

        status = UserProcedure().get_equipment_status_by(equipment_id=equipment_id)

        # かざされたRFIDがDB上貸し出されている場合
        if status == UserProcedure.EquipmentStatus.ALREADY_RESERVED:
            cmn_res.equipment.data = UserProcedure().get_equipment_record_by(equipment_id=equipment_id)
            self.__get_next_state = state.StandbyExpirationDateInputWhenUpdate()

        # かざされたRFIDがDB照合結果、貸し出されているものでなく登録されているものだった場合
        if status == UserProcedure.EquipmentStatus.AVAILABLE:
            Console.puts("まだ貸し出しされていない備品です。", "\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上登録されていない場合
        if status == UserProcedure.EquipmentStatus.NOT_EXIST:
            Console.puts("登録されていない備品です。", "\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDが故障中の場合
        if status == UserProcedure.EquipmentStatus.OUT_OF_ORDER:
            Console.puts("故障中につき貸し出し対象外の備品です。")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください", "\n")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
