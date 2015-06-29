import platform, re
def command_for_current_os(command):
    commandMatch = re.search("\(([^\)]*)\)\s(.*)", command)
    if commandMatch == None:
        return command

    osMatch = re.search(commandMatch.group(1), platform.platform(), re.IGNORECASE)
    if osMatch is None:
        return False

    return commandMatch.group(2)