import random
from rich import print

pelikortit = {'maat': ['♠', '♥', '♦', '♣'], 'arvot': [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]}
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
            pelaajien_valmistus('yksin')
            peli('yksin')
        case 2:
            pelaajien_valmistus('tietokone')
            peli('tietokone')
        case 3:
            pelaajien_valmistus('kaveri')
            peli('kaveri')
        case 4:
            quit()
        case _:
            menu()


def peli(valittu_pelimuoto):
    peli_tiedot['pelimuoto'] = valittu_pelimuoto
    peli_tiedot['vuoro'] = list(pelaajien_tiedot.keys())[0]
    print('\n[bold light_cyan1]Aloitetaan uusi kierros![/bold light_cyan1]')
    aseta_panos()
    jaa_kasi()
    if(valittu_pelimuoto == 'yksin'):
        while(True):
            nayta_tiedot()
            tarkistus = tarkista_voitto()
            match tarkistus[0]:
                case 'Voitto':
                    print(f'{tarkistus[1]} voitti kierroksen!')
                    lisaa_voitto(tarkistus[1])
                    poista_panos(tarkistus[1])
                    peli('yksin')   
                case 'Häviö':
                    print(f'\n[bold red]{tarkistus[1]} - hävisit kierroksen![/bold red]')
                    poista_panos(tarkistus[1])
                    peli('yksin') 
                case 'Jatkuu':
                    continue      
            print(f'\n{peli_tiedot['vuoro']} - Mitä haluat tehdä?')
            print('\n1. Ota kortti\n2. Jako\n3. Tuplaus\n4. Jää\n5. Vakuutus\n6. Antautuminen')
            vastaus = int(input('=> '))
            match vastaus:
                case 1:
                    ota_kortti(peli_tiedot['vuoro'], peli_tiedot['korttipakka'])
                #case 2:
                    #Jako
                #case 3:
                    #Tuplaus
                #case 4:
                    #Jää
                #case 5:
                    #Vakuutus
                #case 6:
                    #Antautuminen
    else:
        counter = 0
        while(counter < 5):
            print(peli_tiedot['vuoro'])
            peli_vuorot()
            counter += 1
                  

def pelaajien_valmistus(valittu_pelimuoto):
    match valittu_pelimuoto:
        case 'yksin':
            pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['jakaja'] = {}, {}
        case 'tietokone':
            pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['tietokone'] = {}, {}
        case 'kaveri':
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
        case _:
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
    peli_tiedot['korttipakka'] = korttipakka
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

def nayta_tiedot():
    print('\nPelaajien tiedot:')
    for pelaaja in pelaajien_tiedot:
        if(pelaaja is not 'jakaja'):
            print(f'\n{pelaaja}n saldo: {pelaajien_tiedot[pelaaja]['saldo']}')
            print(f'{pelaaja}n käsi: {pelaajien_tiedot[pelaaja]['kasi']}')
        else:
            print(f'\nJakajan käsi: {pelaajien_tiedot["jakaja"]['kasi'][0]}, ??????????? ')


def peli_vuorot():
    pelaajat = list(pelaajien_tiedot.keys())
    vuoro = pelaajat.index(peli_tiedot['vuoro'])
    seuraava = vuoro + 1
    if(seuraava > len(pelaajat)-1):
        peli_tiedot['vuoro'] = pelaajat[0]
    else:
        peli_tiedot['vuoro'] = pelaajat[seuraava]


def hae_satunnainen_kortti(korttipakka):
    kortti_indeksi = random.randint(0, len(korttipakka)-1)
    kortti = korttipakka[kortti_indeksi]
    return kortti


def jaa_kasi():
    korttipakka = generoi_korttipakka(pelikortit)
    for pelaaja in pelaajien_tiedot:
        kasi = []
        for i in range(2):
            while(True):
                kortti = hae_satunnainen_kortti(korttipakka)
                if(kortti not in kasi):
                    kasi.append(kortti)
                    korttipakka.remove(kortti)
                    break
                else:
                    continue
        pelaajien_tiedot[pelaaja]['kasi'] = kasi


def ota_kortti(vuoro, korttipakka):
    if(len(pelaajien_tiedot[vuoro]['kasi']) > 4):
        return print('\n[bold red]Voit ottaa enintään viisi (5) korttia per käsi.[/bold red]')
    kortti = hae_satunnainen_kortti(korttipakka)
    pelaajien_tiedot[vuoro]['kasi'].append(kortti)
    peli_tiedot['korttipakka'].remove(kortti)
    return kortti
        
    
def tarkista_voitto():
    for pelaaja in pelaajien_tiedot:
        kaden_arvo = sum([kortti['arvo'] for kortti in pelaajien_tiedot[pelaaja]['kasi']])
        if(kaden_arvo > 21):
            return 'Häviö', pelaaja
        elif(kaden_arvo == 21):
            return 'Voitto', pelaaja
        else:
            return 'Jatkuu'


def lisaa_voitto(pelaaja):
    if(pelaaja is not 'jakaja'):
        pelaajien_tiedot[pelaaja]['saldo'] += pelaajien_tiedot[pelaaja]['panos']

        
def poista_panos(pelaaja):
    if(pelaaja is not 'jakaja'):
        del pelaajien_tiedot[pelaaja]['panos']



   

def tietokone(saldo):
    print(saldo)

aloita_peli()



