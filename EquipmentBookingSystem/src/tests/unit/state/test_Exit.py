#!/usr/bin/env python

import state

from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestExit(TestCase):

    def setUp(self):
        self.state = state.Exit()

    def tearDown(self):
        pass

    def test_exit(self):
        self.state.entry()
        self.state.do()
        self.assertEqual(self.state.should_exit(), False)
        self.assertIsInstance(self.state.get_next_state(), state.Exit)
