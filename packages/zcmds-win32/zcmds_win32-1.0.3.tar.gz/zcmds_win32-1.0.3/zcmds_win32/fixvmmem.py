

from zcmds_win32._exec import os_exec

CMD = 'taskkill /F /im wslservice.exe'


def main() -> int:
    return os_exec(CMD)
