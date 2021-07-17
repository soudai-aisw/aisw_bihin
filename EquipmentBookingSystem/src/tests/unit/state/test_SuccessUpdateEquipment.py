#!/usr/bin/env python

import state
import time

from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestSuccessUpdateEquipment(TestCase):

    def setUp(self):
        self.state = state.SuccessUpdateEquipment()

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
            self.assertIsInstance(self.state.get_next_state(), state.StandbyUserProcedureInput)

    def test_exit_by_time(self):
        # If Timeout shinakattara, state ha exit shinai 
        self.state.entry()
        self.state.do()
        self.assertEqual(self.state.should_exit(), False)


