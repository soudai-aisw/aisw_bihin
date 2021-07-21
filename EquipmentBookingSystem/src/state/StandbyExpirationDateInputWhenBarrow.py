#!/usr/bin/env python



import time
import state as state
import dev.display.Console as Console
import dev.input as input

class StandbyExpirationDateInputWhenBarrow(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("返却予定日を入力してください(yyyy/mm/dd)")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        return_date = self.__input.get_string()
        Console.puts("返却予定日",return_date,"を受理しました")
        time.sleep(1.500)
        state.CommonResource.expirationDate = return_date

    def get_next_state(self):
        return state.SuccessBarrowEquipment()

    def should_exit(self):
        return self.__input.submitted()
