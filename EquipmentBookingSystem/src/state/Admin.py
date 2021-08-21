#!/usr/bin/env python

from state.commonResource import CommonResource
import time
import hashlib
import pandas as pd

import state as state
import dev.display.Console as Console
import dev.input as input

from config import *

from enum import Enum, auto


class Command(Enum):
    FATAL = auto()
    INVALID_CMD = auto()
    INVALID_ARG = auto()
    EXIT = auto()
    SHOW_USER = auto()
    SHOW_EQUIPMENT = auto()
    ADD_EQUIPMENT = auto()
    SHOW_HELP = auto()


class Admin(state.IState):
    def entry(self):
        self.__text_field = input.ConsoleTextField()

        if not isinstance(CommonResource.prev_state, state.Admin):
            Console.puts("")
            Console.puts("[Start admin mode]")

        Console.puts("# ", end="")

    def do(self):
        self.__text_field.capture()

    def exit(self):
        cmd = self.__analize_command()
        self.__cmd = cmd

        if cmd == Command.FATAL:
            Console.puts("Faital Error !!")
        elif cmd == Command.INVALID_CMD:
            Console.puts("Command error !! It is invalid command.")
        elif cmd == Command.INVALID_ARG:
            Console.puts("Command error !! It is invalid arguments.")
        elif cmd == Command.EXIT:
            Console.puts("Bye !")
        elif cmd == Command.SHOW_USER:
            Console.puts(pd.read_csv(get_user_db_path(), encoding="cp932"))
        elif cmd == Command.SHOW_EQUIPMENT:
            Console.puts(pd.read_csv(
                get_equipment_db_path(), encoding="cp932"))
        elif cmd == Command.ADD_EQUIPMENT:
            Console.puts("Add equipment command is not implemented yet.")
        elif cmd == Command.SHOW_HELP:
            Console.puts("exit        Exit Admin Mode")
            Console.puts("show[-opt]  Show List -u:Users -e:Equipment")
            Console.puts("add[-opt]   Add Item  -e:Equipmet")

    def get_next_state(self):
        if self.__cmd == Command.EXIT:
            return state.Init()
        else:
            return state.Admin()

    def should_exit(self):
        return self.__text_field.submitted()

    def __analize_command(self):
        commands = self.__text_field.get_string().split()

        try:
            if commands[0] == "exit" or commands[0] == "bye":
                return Command.EXIT
            if commands[0] == "show":
                if commands[1] == "-u":
                    return Command.SHOW_USER
                elif commands[1] == "-e":
                    return Command.SHOW_EQUIPMENT
                else:
                    return Command.INVALID_ARG

            if commands[0] == "add":
                if commands[1] == "-e":
                    return Command.ADD_EQUIPMENT
                else:
                    return Command.INVALID_ARG

            if commands[0] == "help":
                return Command.SHOW_HELP

            else:
                return Command.INVALID_CMD

        except:
            return Command.FATAL
