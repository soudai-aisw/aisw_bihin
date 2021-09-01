#!/usr/bin/env python

class Record():
    def __init__(self):
        self.__dict = self._dict_init()

    @property
    def data(self) -> dict:
        return self.__dict

    @data.setter
    def data(self, a_dict: dict):
        for key, value in a_dict.items():
            if key not in self.__dict:
                raise KeyError("The key '" + key + "' does not exist.")
            if not self._validate(key, value):
                raise ValueError("The value '" + value + "' does not accept.")
            self.__dict[key] = value

    def _dict_init(self):
        raise NotImplementedError(
            "Record must define '_dict_init' to use this base class")

    def _validate(self, key, value):
        raise NotImplementedError(
            "Record must define '_validate' to use this base class")
