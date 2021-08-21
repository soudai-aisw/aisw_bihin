#!/usr/bin/env python


import time
import state as state
import dev.display.Console as Console
import dev.input as input


class PreExit(state.IState):

    def entry(self):
        state.CommonResource.initialize()
        self.__pressed_key = input.PressedKey()
        Console.puts("エントランスでESCキーが入力されました。")
        Console.puts("タイムアウト前にもう一度ESCキーを入力すると完全にプログラムを終了します。")

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        if self.__pressed_key.is_escape():
            return state.Exit()
        else:
            return state.Init()

    def should_exit(self):
        return self.__pressed_key.exists()
