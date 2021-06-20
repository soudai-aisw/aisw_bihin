#!/usr/bin/env python

import platform
import os
import sys


def clear():
    # プラットフォームに応じてシステムコマンドを使い分ける
    if (platform.system() == 'Windows'):
        os.system('cls')
    else:
        os.system('clear')


def puts(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    # printのラッパー。必要に応じてここにロギング処理を記述ことも可能
    print(*objects, sep=sep, end=end, file=file, flush=flush)
    sys.stdout.flush()


def remove_line():
    sys.stdout.write("\033[2K\033[G")
    sys.stdout.flush()


def remove_char():
    sys.stdout.write("\033[1D\033[K")
    sys.stdout.flush()


def debug_this_module():

    clear()
    time.sleep(0.5)

    puts("1abc", end="")
    time.sleep(0.5)

    remove_line()
    time.sleep(0.5)

    puts("2abc", end="")
    time.sleep(0.5)

    remove_char()
    time.sleep(0.5)

    puts("3abc", end="")
    time.sleep(0.5)

    clear()
    time.sleep(1)


if __name__ == "__main__":
    import time

    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
