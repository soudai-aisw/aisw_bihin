#!/usr/bin/env python
import os

# path
def is_release_mode():
    return False

def is_debug_mode():
    return True

# path
def get_project_root():
    return os.path.join(get_src_dir(), "..")

def get_src_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_database_dir():
    return os.path.join(get_project_root(), "resource/database")

def get_user_db_path():
    return os.path.join(get_database_dir(), "t_user.csv")

def get_equipment_db_path():
    return os.path.join(get_database_dir(), "t_equipment.csv")

# time
def get_time_of_main_cycle():
    return 0.010

def get_time_of_timeout():
    return 30

def get_time_of_message_display():
    return 3

def get_time_of_error_display():
    return 5

# login
def get_key_of_to_enter_login_form():
    return b'A'

def get_hashed_login_password_with_salt():
    return '0936eabb96a04812fe0b3729a784264b'


