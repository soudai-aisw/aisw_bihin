#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
import db.matching.DBmatching as db


class StandbyUpdateEquipmentIdInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("更新する機材のIDをキーボードで入力してください")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        # キーボード入力受付（Enterが押されたらexitへ移行する）
        self.__input.capture()

    def exit(self):
        # キーボード情報取得
        key_data = self.__input.get_string()

        # -----DBの戻り値-----
        # 0: 未登録
        # 1：借用可能
        # 2：借用中
        # 3：故障中
        # --------------------

        rfid_return = db.DBmatching_EquIDtoEquStatus(key_data)

        # かざされたRFIDがDB上貸し出されている場合
        if rfid_return == 2:
            state.CommonResource.equipmentId = key_data
            self.__get_next_state = state.StandbyExpirationDateInputWhenUpdate()

        # かざされたRFIDがDB照合結果、貸し出されているものでなく登録されているものだった場合
        if rfid_return == 1:
            Console.puts("まだ貸し出しされていない備品です。", "\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上登録されていない場合
        if rfid_return == 0:
            Console.puts("登録されていない備品です。", "\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDが故障中の場合(今は仮値)
        if rfid_return == 3:
            Console.puts("故障中につき貸し出し対象外の備品です。")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください", "\n")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
