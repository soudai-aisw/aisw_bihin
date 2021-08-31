#!/usr/bin/env python
import pandas
import shutil
import datetime


class Ledger():
    def __init__(self, backup=False):
        if backup:
            #shutil.copyfile(self._db_path,self._db_path+".{0:%Y%m%d_%H%M%S}".format(datetime.datetime.now()))
            shutil.copyfile(self._db_path,self._db_path+".{0:%Y%m%d_%Hh}".format(datetime.datetime.now()))

    def query(self, query):
        if query == "*":
            return self.__read_all()
        else:
            return self.__read_all().query(query)

    def find(self, query):  # Syntax suger for query
        return self.query(query)

    def append(self, record):
        if not isinstance(record, self._acceptable_object):
            return False
        if len(self.find_by(self._primary_key, record.data[self._primary_key])) != 0:
            return False
        return self.__write_all(self.__read_all().append(record.data, ignore_index=True))

    def update(self, record):
        if not isinstance(record, self._acceptable_object):
            return False
        target = self.find_by(
            self._primary_key, record.data[self._primary_key])
        if len(target) != 1:
            return False
        records = self.__read_all()
        records.loc[target.index.values[0]] = record.data
        return self.__write_all(records)

    def drop_by(self, key, value):
        return self.__write_all(self.query('{0} != "{1}"'.format(key, value)))

    def find_by(self, key, value):
        return self.query('{0} == "{1}"'.format(key, value))

    def __read_all(self):
        return pandas.read_csv(self._db_path, encoding=self._encoding, dtype=object)

    def __write_all(self, records):
        records.to_csv(self._db_path, index=False,
                       header=True, encoding=self._encoding, mode='w')
        return True

    @property
    def _db_path(self):
        raise NotImplementedError(
            "Ledger must define '_db_path' to use this base class")

    @property
    def _encoding(self):
        raise NotImplementedError(
            "Ledger must define '_encoding' to use this base class")

    @property
    def _primary_key(self):
        raise NotImplementedError(
            "Ledger must define '_primary_key' to use this base class")

    @property
    def _acceptable_object(self):
        raise NotImplementedError(
            "Ledger must define '_acceptable_object' to use this base class")
