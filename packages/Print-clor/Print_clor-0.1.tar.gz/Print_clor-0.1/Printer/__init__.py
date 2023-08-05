from colorama import Fore, Back, Style

def printfn(Text):
    print(Text)

def printRed(Text):
    print(Fore.RED + Text + Style.RESET_ALL)

def printGreen(Text):
    print(Fore.GREEN + Text + Style.RESET_ALL)

def printYellow(Text):
    print(Fore.YELLOW + Text + Style.RESET_ALL)

def printBlue(Text):
    print(Fore.BLUE + Text + Style.RESET_ALL)

def printBlack(Text):
    print(Fore.BLACK + Text + Style.RESET_ALL)

def printError(Text):
    print(Back.RED + Style.BRIGHT + Fore.WHITE + Text + Style.RESET_ALL)
