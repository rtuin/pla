import platform
import re


def command_for_current_os(command):
    command_match = re.search("\(([^\)]*)\)\s(.*)", command)
    if command_match is None:
        return command

    os_match = re.search(command_match.group(1), platform.platform(), re.IGNORECASE)
    if os_match is None:
        return False

    return command_match.group(2)
