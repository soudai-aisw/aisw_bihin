#!/usr/bin/env python

import time

import state as state
import dev.display.Console as Console
import dev.input as input
import config
from state.commonResource import CommonResource as cmn_res

class Init(state.IState):

    def entry(self):
        cmn_res.initialize()
        self.__pressed_key = input.PressedKey()
        Console.clear()
        Console.puts("備品管理システムにようこそ")
        Console.puts("何かキーを押すとサービスを開始します")

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        if self.__pressed_key.is_escape():
            return state.PreExit()
        elif self.__pressed_key.get() == config.get_key_of_to_enter_login_form():
            return state.LoginAsAdmin()
        else:
            return state.StandbyUserIdInput()

    def should_exit(self):
        return self.__pressed_key.exists()
