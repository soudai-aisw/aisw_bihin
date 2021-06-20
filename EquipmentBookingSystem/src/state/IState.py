#!/usr/bin/env python


import abc


class IState(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def entry(self):
        raise NotImplementedError(
            "users must define 'entry' to use this base class")

    @abc.abstractmethod
    def do(self):
        raise NotImplementedError(
            "users must define 'do' to use this base class")

    @abc.abstractmethod
    def exit(self):
        raise NotImplementedError(
            "users must define 'exit' to use this base class")

    @abc.abstractmethod
    def get_next_state(self):
        raise NotImplementedError(
            "users must define 'get_next_state' to use this base class")

    @abc.abstractmethod
    def should_exit(self):
        raise NotImplementedError(
            "users must define 'should_exit' to use this base class")
