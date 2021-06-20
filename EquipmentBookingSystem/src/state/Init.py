#!/usr/bin/env python

import time

import state as state
import dev.display.Console as Console
import dev.input as input


class Init(state.IState):

    def entry(self):
        state.CommonResource.initialize()
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
        else:
            return state.StandbyUserIdInput()

    def should_exit(self):
        return self.__pressed_key.exists()

