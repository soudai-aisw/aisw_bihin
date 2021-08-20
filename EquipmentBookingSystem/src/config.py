#!/usr/bin/env python
import os

def get_project_root():
    return os.path.join(get_src_dir(), "..")

def get_src_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_database_dir():
    return os.path.join(get_project_root(), "database")

def get_user_db_path():
    return os.path.join(get_database_dir(), "db_userlist.csv")

def get_equipment_db_path():
    return os.path.join(get_database_dir(), "db_itemlist.csv")
