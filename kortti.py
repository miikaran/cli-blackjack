from colorama import Fore, Back, Style, init

def tulosta_kortti(rank, suit):
    kortin_vari = Back.WHITE if suit in ['♥', '♦'] else Back.BLACK
    print(f"{Fore.RED}{kortin_vari} {rank} {suit} {Style.RESET_ALL}", end=" ")
