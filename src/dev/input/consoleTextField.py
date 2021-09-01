#!/usr/bin/env python


if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')


import dev.display.Console as Console
import dev.input as input
from logging import getLogger


class ConsoleTextField(input.IUserInputReader):
    """コンソール画面上でキーボードから文字列を受け取るクラスです。

    captureメソッドを周期的にコールしてキーボード入力を監視してください。
    エンターキーが押下されたとき、submittedがTrueとなります。
    ユーザが入力した文字列はget_stringを用いて受け取ることができます。

    Examples:

        >>> consoleTextField = ConsoleTextField()
        >>> while not consoleTextField.submitted(): # エンターキーが入力されるまで繰り返す
        >>>     consoleTextField.capture()          # キーボード入力を監視する
        >>>     time.sleep(0.010)
        >>> print(consoleTextField.get_string())    # 入力された文字列を表示する
        Hello !!
    """

    def __init__(self):
        self.__logger = getLogger(__name__)

        self._pressed_key = input.PressedKey()
        self._string = ""
        self._submitted = False
        self._is_real_time_display_mode = True

    def capture(self):
        """キーボード入力を監視します。

        Args:
            (void): 無し

        Returns:
            void

        Note:
            singletonKeyboardスレッドの実行周期より遅い場合、入力を取りこぼす可能性があります。

        """

        self._pressed_key.capture()

        if self._pressed_key.exists():

            if self._pressed_key.is_enter():
                # Submit keyboard input
                self._submitted = True
                if self._is_real_time_display_mode:
                    Console.puts("")  # New line
                self.__logger.info("The user entered '%s'", self._string)

            elif self._pressed_key.is_escape():
                # Clear buffer
                self._string = ""
                if self._is_real_time_display_mode:
                    Console.remove_line()

            elif self._pressed_key.is_delete():
                # Remove a last charcter
                if (len(self._string) > 0):
                    self._string = self._string[:-1]
                    if self._is_real_time_display_mode:
                        Console.remove_char()
            else:
                # Join a character to last position
                key = chr(ord(self._pressed_key.get()))
                if key.isascii():
                    self._string += key
                    if self._is_real_time_display_mode:
                        Console.puts(key, end='')

        else:
            self._updated = False

    def get_string(self):
        """バッファに蓄積されている文字列を返します。

        Args:
            (void): 無し

        Returns:
            str: バッファに蓄積されている文字列

        """
        return self._string

    def submitted(self):
        """エンターキーが押されたときTrueを返します。

        Args:
            (void): 無し

        Returns:
            bool: エンターキーが押されたか

        """
        return self._submitted

    def display_in_real_time(self, enabled):
        """キーボード入力をリアルタイムにコンソール出力すべきか否かを切り替えます。

        Args:
            enabled (bool): Trueであればリアルタイム出力を行います。

        Returns:
            void

        """
        self._is_real_time_display_mode = enabled


def debug_this_module():
    Console.clear()

    text_field = ConsoleTextField()

    while not text_field.submitted():
        text_field.capture()
        time.sleep(0.010)

    Console.puts("Your input is :", text_field.get_string())
    time.sleep(3)

    del text_field


if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
