#!/usr/bin/env python


import abc


class IUserInputReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError(
            "users must define '__init__' to use this base class")

    @abc.abstractmethod
    def capture(self):
        raise NotImplementedError(
            "users must define 'capture' to use this base class")

    @abc.abstractmethod
    def get_string(self):
        raise NotImplementedError(
            "users must define 'get_string' to use this base class")

    @abc.abstractmethod
    def submitted(self):
        raise NotImplementedError(
            "users must define 'submitted' to use this base class")
