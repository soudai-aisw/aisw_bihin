#!/usr/bin/env python

import state

from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestErrorHasOccurred(TestCase):

    def setUp(self):
        self.state = state.ErrorHasOccurred()

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
        # Link with CommonResource.prev_state
        state.CommonResource.prev_state = state.Init()
        self.assertIsInstance(self.state.get_next_state(), state.Init)

        state.CommonResource.prev_state = state.Restart()
        self.assertIsInstance(self.state.get_next_state(), state.Restart)

    def test_exit_by_timeout(self):
        timeout = 3

        # Test the conditions of exit from this state.
        with patch("time.time") as mock_time:
            # Initialize before entry
            mock_time.return_value = 0
            self.state.entry()

            # Just the same time when enter this state.
            mock_time.return_value = 0
            self.state.do()
            self.assertEqual(self.state.should_exit(), False)

            # Before 'timeout' seconds have passed.
            mock_time.return_value = timeout - 0.1
            self.state.do()
            self.assertEqual(self.state.should_exit(), False)

            # Just 'timeout' seconds.
            mock_time.return_value = timeout
            self.state.do()
            self.assertEqual(self.state.should_exit(), False)

            # Elapsed 'timeout' seconds.
            mock_time.return_value = timeout + 0.1
            self.state.do()
            self.assertEqual(self.state.should_exit(), True)

        # Test the state of the next transition destination.
        # Link with CommonResource.prev_state
        state.CommonResource.prev_state = state.Init()
        self.assertIsInstance(self.state.get_next_state(), state.Init)

        state.CommonResource.prev_state = state.Restart()
        self.assertIsInstance(self.state.get_next_state(), state.Restart)