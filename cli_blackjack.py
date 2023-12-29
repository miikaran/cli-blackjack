import random
from rich import print

pelikortit = {
    'maat': ['♠', '♥', '♦', '♣'],
    'arvot': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] 
}
pelimuoto = ''
vuoro = ''
pelaaja_tiedot = {}


def aloita_peli():
    menu()


def menu():
    print('\n[bold red]Tervetuloa pelaamaan komentolinja Blackjackkia! [/bold red]')
    print('[cyan3]Valitse numeroilla pelimuoto, jota haluat pelata.[/cyan3]\n')
    print('1. [bold light_cyan1]Yksin[/bold light_cyan1]\n2. [bold light_cyan1]Tietokonetta vastaan[/bold light_cyan1]\n3. [bold light_cyan1]Kavereita vastaan[/bold light_cyan1]\n4. [bold bright_red]Lopeta peli[/bold bright_red]\n')
    pelimuoto = int(input('=>  '))
    if(pelimuoto == 1):
        peli('yksin')
    elif(pelimuoto == 2):
        peli('tietokone')
    elif(pelimuoto == 3):
            peli('kaveri')
    elif(pelimuoto == 4):
        quit()


def peli(pelimuoto):
    generoi_korttipakka(pelikortit)
    if(pelimuoto == 'tietokone' or pelimuoto == 'kaveri'):
        pelaajien_valmistus(pelimuoto)


def pelaajien_valmistus(pelimuoto):
    if(pelimuoto == 'kaveri'):
        print('\nLisätään pelaajia peliin.')
        jarjestys = 1 
        while(True):   
            print('Kirjoita S tallentaaksesi lisäyksesi\n')
            nimi = input(f'\n{jarjestys}. pelaajan nimi: ')
            if(nimi == 'S' or nimi == 's'):
                if(len(pelaaja_tiedot) > 1):
                    print('Tallennetaanko pelaajat:')
                    for i in pelaaja_tiedot:
                        print(i)
                    varmistus = input('Kylla/Ei? => ')
                    if(varmistus.lower() == 'kylla'):
                        break
                    elif(varmistus.lower() == 'ei'):
                        continue
                break
            pelaaja_tiedot[nimi] = {'jarjestys': jarjestys}
            jarjestys += 1        
    return pelaaja_tiedot


def generoi_korttipakka(pelikortit):
    korttipakka = []
    for i in range(len(pelikortit['maat'])):
        for j  in range(len(pelikortit['arvot'])):
            kortti = {
                'maa': pelikortit['maat'][i], 
                'arvo': pelikortit['arvot'][j]
            }
            korttipakka.append(kortti) 
    korttipakka = sekoita_korttipakka(korttipakka)
    return korttipakka


def sekoita_korttipakka(korttipakka):
    sekoitettu_korttipakka = korttipakka
    random.shuffle(sekoitettu_korttipakka)
    '''Oma koodin pätkä korttipakan sekoittamiselle. (very good time complexity yes)

    for i in range(len(korttipakka)):
        kortti = korttipakka[random.randint(0, len(korttipakka) - 1)]
        if(kortti in sekoitettu_korttipakka):
            while(kortti in sekoitettu_korttipakka):
                kortti = korttipakka[random.randint(0, len(korttipakka) - 1)]
                if(kortti not in sekoitettu_korttipakka):
                        sekoitettu_korttipakka.append(kortti)
                        break
        else:
            sekoitettu_korttipakka.append(kortti)
    '''
    return sekoitettu_korttipakka


aloita_peli()



