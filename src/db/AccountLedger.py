from db.AccountRecord import AccountRecord
from db import Ledger
import config


class AccountLedger(Ledger):
    @property
    def _db_path(self):
        return config.get_user_db_path()

    @property
    def _encoding(self):
        return "shift-jis"

    @property
    def _primary_key(self):
        return AccountRecord.EMPLOYEE_ID

    @property
    def _acceptable_object(self):
        return AccountRecord
