import random
from rich import print

pelikortit = {
    'maat': ['♠', '♥', '♦', '♣'],
    'arvot': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] 
}
peli_tiedot = {}
pelaajien_tiedot = {}


def aloita_peli():
    menu()


def menu():
    print('\n[bold red]Tervetuloa pelaamaan komentolinja Blackjackkia! [/bold red]')
    print('[cyan3]Valitse numeroilla pelimuoto, jota haluat pelata.[/cyan3]\n')
    print('1. [bold light_cyan1]Yksin[/bold light_cyan1]\n2. [bold light_cyan1]Tietokonetta vastaan[/bold light_cyan1]\n3. [bold light_cyan1]Kavereita vastaan[/bold light_cyan1]\n4. [bold bright_red]Lopeta peli[/bold bright_red]\n')
    while(True):
        try:
            valitse_pelimuoto = int(input('=> '))
            break
        except:
            print('Virheellinen valinta')
            menu()
    match valitse_pelimuoto:
        case 1:
            peli('yksin')
        case 2:
            peli('tietokone')
        case 3:
            peli('kaveri')
        case 4:
            quit()
        case _:
            menu()


def peli(valittu_pelimuoto):
    peli_tiedot['pelimuoto'] = valittu_pelimuoto
    pelaajien_valmistus(valittu_pelimuoto)
    print('\n[bold light_cyan1]Aloitetaan kierros![/bold light_cyan1]')
    aseta_panos()
    jaa_kasi(valittu_pelimuoto)
    if(valittu_pelimuoto == 'yksin'):
        while(True):
            print(f'\nPelaajan käsi: {pelaajien_tiedot['Pelaaja']['käsi']}')
            print(f'Jakajan käsi: {pelaajien_tiedot["jakaja"]['käsi'][0]}, ??????????? ')
            print('\n Haluatko ')
        
        
def pelaajien_valmistus(valittu_pelimuoto):
    if(valittu_pelimuoto == 'yksin'):
        pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['jakaja'] = {}, {}
    elif(valittu_pelimuoto == 'tietokone'):
        pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['tietokone'] = {}, {}
    elif(valittu_pelimuoto == 'kaveri'):
        print('\n[bold red]Lisätään pelaajia peliin.[/bold red]')
        jarjestys = 1 
        while(True):   
            print('[cyan3]Kirjoita S tallentaaksesi lisäyksesi[/cyan3]\n')
            nimi = input(f'\n{jarjestys}. pelaajan nimi: ')
            if(nimi == 'S' or nimi == 's'):
                if(len(pelaajien_tiedot) > 0):
                    print('Tallennetaanko pelaajat?')
                    for i in pelaajien_tiedot:
                        print(i)
                    varmistus = input('Kylla/Ei? => ')
                    if(varmistus.lower() == 'kylla'):
                        break
                    elif(varmistus.lower() == 'ei'):
                        continue
                    else:
                        continue
                break
            if(nimi == None or nimi == ''):
                print('[bold red]Älä jätä pelaajan nimeä tyhjäksi[/bold red]\n')
                continue
            else:
                pelaajien_tiedot[nimi] = {'jarjestys': jarjestys}
                jarjestys += 1
    else:
        menu()
    for pelaaja in pelaajien_tiedot:
        if(pelaaja is not 'jakaja'):
            pelaajien_tiedot[pelaaja]['saldo'] = 500
    return pelaajien_tiedot


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


def aseta_panos():
    for pelaaja in pelaajien_tiedot:
        if(pelaaja is not 'tietokone' and pelaaja is not 'jakaja'):
            print(f'\n{pelaaja}: Aseta panos kierrokselle!')
            while(True):
                try:
                    panos = int(input('=> '))
                except:
                    print('Virheellinen panos')
                    continue
                virheellinen_panos = panos > pelaajien_tiedot[pelaaja]['saldo'] or panos <= 0
                if(virheellinen_panos):
                    print('Yritä uudelleen')
                    continue
                else:
                    pelaajien_tiedot[pelaaja]['saldo'], pelaajien_tiedot[pelaaja]['panos'] = pelaajien_tiedot[pelaaja]['saldo'] - panos, panos
                    break
        elif(pelaaja == 'tietokone'):
            tietokone(pelaajien_tiedot[pelaaja]['saldo'])


def jaa_kasi(valittu_pelimuoto):
    korttipakka = generoi_korttipakka(pelikortit)
    for pelaaja in pelaajien_tiedot:
        käsi = []
        for i in range(2):
            while(True):
                kortti_indeksi = random.randint(0, len(korttipakka))
                kortti = korttipakka[kortti_indeksi]
                if(kortti not in käsi):
                    käsi.append(kortti)
                    korttipakka.remove(kortti)
                    #korttipakka.remove(kortti)
                    break
                else:
                    continue
        pelaajien_tiedot[pelaaja]['käsi'] = käsi
   

def tietokone(saldo):
    print(saldo)

aloita_peli()



