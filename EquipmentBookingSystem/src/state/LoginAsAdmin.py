#!/usr/bin/env python

import time
import hashlib

import state as state
import dev.display.Console as Console
import dev.input as input

class LoginAsAdmin(state.IState):
    def entry(self):
        self.__text_field = input.ConsoleTextField()
        Console.clear()
        Console.puts("[Login as admin]")
        Console.puts("Please enter the password.")
        Console.puts(">", end="")

    def do(self):
        self.__text_field.capture()

    def exit(self):
        pass

    def get_next_state(self):
        if self.__hasSuccessLoggedIn():
            Console.puts("Login success.")
            return state.Admin()
        else:
            Console.puts("Login failed.")
            next = state.GotoNextAfterWaiting()
            next.set_next_state(state.LoginAsAdmin())
            return next

    def should_exit(self):
        return self.__text_field.submitted()

    def __hasSuccessLoggedIn(self):
        raw_pw = "#" + self.__text_field.get_string() + "#"
        hashed_pw = hashlib.md5(hashlib.md5(raw_pw.encode()).hexdigest().encode()).hexdigest()

        return hashed_pw == '0936eabb96a04812fe0b3729a784264b'
