import json
import os
from enum import Enum


_users_key = 'users'
_admin_id_key = 'admin_id'
_printer_name_key = 'printer_name'


class _UsersStatus(Enum):
    allowed = 'allowed'
    pending = 'pending'


class PrintBotConfig:
    def __init__(self):
        self._config_file = '.printbot/config.json'
        if not os.path.exists(self._config_file):
            self._create_default_config()
        with open(self._config_file, 'r') as f:
            self._config = json.load(f)

    def _create_default_config(self):
        os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
        default = {
            _admin_id_key: 1234567890,
            _printer_name_key: "",
            _users_key: {
            }
        }
        with open(self._config_file, 'w') as f:
            json.dump(default, f, indent=4)

    def save_config(self):
        with open(self._config_file, 'w') as f:
            json.dump(self._config, f, indent=4)

    def admin_id(self):
        return self._config[_admin_id_key]

    def is_admin(self, user_id: int) -> bool:
        return user_id == self._config[_admin_id_key]

    def is_user_allowed(self, user_id: int) -> bool:
        status = self._config.get(_users_key, {}).get(str(user_id))
        return status == _UsersStatus.allowed.value or self.is_admin(user_id)

    def is_user_pending(self, user_id: int) -> bool:
        return self._config.get(_users_key, {}).get(str(user_id)) == _UsersStatus.pending.value

    def add_pending_user(self, user_id: int):
        if str(user_id) not in self._config.get(_users_key, {}):
            self._config.setdefault(_users_key, {})[str(user_id)] = _UsersStatus.pending.value
            self.save_config()

    def approve_user(self, user_id: int):
        if str(user_id) in self._config.get(_users_key, {}):
            self._config[_users_key][str(user_id)] = _UsersStatus.allowed.value
            self.save_config()

    def reject_user(self, user_id: int):
        if str(user_id) in self._config.get(_users_key, {}):
            del self._config[_users_key][str(user_id)]
            self.save_config()

    def get_printer_name(self) -> str:
        return self._config.get('printer_name', '')