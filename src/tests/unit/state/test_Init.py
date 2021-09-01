#!/usr/bin/env python

import state

from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestInit(TestCase):

    def setUp(self):
        self.state = state.Init()

    def tearDown(self):
        pass

    def test_exit_by_key(self):
        self.state.entry()

        # Test the conditions of exit from this state.
        with patch("dev.input.PressedKey.exists") as mock_pressedKey_exists:
            # If pressed key does not exists, state should not exit.
            mock_pressedKey_exists.return_value = False
            self.state.do()
            self.assertEqual(self.state.should_exit(), False)

            # If pressed key exists, state should exit.
            mock_pressedKey_exists.return_value = True
            self.state.do()
            self.assertEqual(self.state.should_exit(), True)

        # Test the state of the next transition destination.
        with patch("dev.input.PressedKey.is_escape") as mock_pressedKey_is_escape:
            # if pressed key is not espace, next state is Init.
            mock_pressedKey_is_escape.return_value = False
            self.state.do()
            self.assertIsInstance(
                self.state.get_next_state(), state.StandbyUserIdInput)

            # if pressed key is espace, next state is Exit.
            mock_pressedKey_is_escape.return_value = True
            self.state.do()
            self.assertIsInstance(self.state.get_next_state(), state.PreExit)
