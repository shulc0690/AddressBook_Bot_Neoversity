from colorama import Fore, Back, Style


def main_msg(message):
    print(Fore.GREEN + message + Style.RESET_ALL)


def main_msg4return(message):
    return Fore.GREEN + message + Style.RESET_ALL


def error_msg(message):
    print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)


def error_msg4return(message):
    return Fore.RED + Style.BRIGHT + message + Style.RESET_ALL


def info_msg(message):
    print(Fore.GREEN, Style.BRIGHT + message + Style.RESET_ALL)


def info_msg4return(message):
    return Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL


def table_style(message):
    print(Fore.GREEN + message)


def logo_style(message):
    print(Fore.YELLOW + message)


def angry_style(message):
    print(Fore.RED + Style.DIM + message + Style.RESET_ALL)


def angry_style4return(message):
    return Fore.RED + Style.DIM + message + Style.RESET_ALL
