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
    
    while True:
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

    while True:     
        nayta_tiedot()
        
        if valittu_pelimuoto == 'yksin':
            automaattinen_voitto = tarkista_voitto(False)          
            if automaattinen_voitto != 'Jatkuu':
                peli('yksin')

        print(f'\n{peli_tiedot['vuoro']} - Mitä haluat tehdä?')
        print('\n1. Ota kortti\n2. Jako\n3. Tuplaus\n4. Jää\n5. Vakuutus\n6. Antautuminen')
        
        vastaus = int(input('=> '))

        match vastaus:
            case 1:
                ota_kortti(peli_tiedot['vuoro'], peli_tiedot['korttipakka'])
            #case 2:
                #Jako
            case 3:
                tuplaa(peli_tiedot['vuoro'])
            case 4:
                jää(valittu_pelimuoto, peli_tiedot['vuoro'])              
            #case 5:
                #Vakuutus
            #case 6:
                #Antautuminen
    
                  
def pelaajien_valmistus(valittu_pelimuoto):
    match valittu_pelimuoto:
        case 'yksin':
            pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['jakaja'] = {}, {}
        case 'tietokone':
            pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['tietokone'] = {}, {}
        case 'kaveri':
            print('\n[bold red]Lisätään pelaajia peliin.[/bold red]')
            pelaaja_jarjestys = 1 

            while True:   
                print('[cyan3]Kirjoita S tallentaaksesi lisäyksesi[/cyan3]\n')
                nimi = input(f'\n{pelaaja_jarjestys}. pelaajan nimi: ')

                if nimi.lower() == 's':
                    if len(pelaajien_tiedot) > 0:
                        print('Tallennetaanko pelaajat?')
                        for pelaaja in pelaajien_tiedot:
                            print(pelaaja)
                        varmistus = input('Kylla/Ei? => ').lower()
                        if varmistus == 'kylla':
                            break
                        elif varmistus == 'ei':
                            continue
                        else:
                            continue
                    break
                if nimi == None or nimi == '':
                    print('[bold red]Älä jätä pelaajan nimeä tyhjäksi[/bold red]\n')
                    continue
                else:
                    pelaajien_tiedot[nimi] = {'jarjestys': pelaaja_jarjestys}
                    pelaaja_jarjestys += 1
        case _:
            menu()

    for pelaaja in pelaajien_tiedot:
        if pelaaja != 'jakaja':
            pelaajien_tiedot[pelaaja]['saldo'] = 500

    return pelaajien_tiedot


def generoi_korttipakka(pelikortit):
    korttipakka = [
        {'maa': maa, 'arvo': arvo}
        for maa in pelikortit['maat']
        for arvo in pelikortit['arvot']
    ]
    korttipakka = sekoita_korttipakka(korttipakka)
    peli_tiedot['korttipakka'] = korttipakka
    return korttipakka


def sekoita_korttipakka(korttipakka):
    sekoitettu_korttipakka = korttipakka
    random.shuffle(sekoitettu_korttipakka)
    return sekoitettu_korttipakka


def aseta_panos():
    for pelaaja in pelaajien_tiedot:
        tiedot = pelaajien_tiedot[pelaaja]
        if pelaaja != 'tietokone' and pelaaja != 'jakaja':
            print(f'\nSinulla on {tiedot['saldo']}$\n{pelaaja}: Aseta panos kierrokselle!')
            while True:
                try:
                    panos_input = int(input('=> '))
                except ValueError:
                    print('Virheellinen panos')
                    continue

                if panos_input <= 0 or panos_input > tiedot['saldo']:
                    print('Virheellinen panos. Yritä uudelleen')
                    continue
                else:
                    tiedot['saldo'], tiedot['panos'] = tiedot['saldo']-panos_input, panos_input
                    break
        elif pelaaja == 'tietokone':
            tietokone(tiedot['saldo'])

def nayta_tiedot():
    print('\nPelaajien tiedot:')

    for pelaaja in pelaajien_tiedot:
        tiedot = pelaajien_tiedot[pelaaja]
        if pelaaja != 'jakaja':
            try:
                pelaajan_saldo = tiedot['saldo'] + tiedot['panos']
                print(f'\n{pelaaja}n saldo: {pelaajan_saldo}$')
                print(f'{pelaaja}n panos: {tiedot['panos']}$')
                print(f'{pelaaja}n käsi: {tiedot['kasi']}')
            except KeyError:
                pass
        else:
            try:
                print(f'\nJakajan käsi: {tiedot['kasi']}')
            except KeyError:
                pass


def peli_vuorot():
    pelaajat = list(pelaajien_tiedot.keys())
    vuoro_index = pelaajat.index(peli_tiedot['vuoro'])
    seuraava = vuoro_index+1

    if seuraava > len(pelaajat)-1:
        tarkista_voitto(True)
        peli_tiedot['vuoro'] = pelaajat[0]
    else:
        peli_tiedot['vuoro'] = pelaajat[seuraava]


def hae_satunnainen_kortti(korttipakka):
    kaytetyt_kortit = peli_tiedot['kaytetyt_kortit']
    while True:
        kortti = random.choice(korttipakka)
        if kortti not in kaytetyt_kortit:
            kaytetyt_kortit.append(kortti)
            return kortti


def jaa_kasi():
    korttipakka = generoi_korttipakka(pelikortit)
    peli_tiedot['kaytetyt_kortit'] = []

    for pelaaja in pelaajien_tiedot:
        pelaajan_tiedot = pelaajien_tiedot[pelaaja]
        kasi = [hae_satunnainen_kortti(korttipakka) for _ in range(2)]
        pelaajan_tiedot['kasi'] = kasi


def ota_kortti(vuoro, korttipakka):
    max_kortit = 4
    pelaaja_tiedot = pelaajien_tiedot[vuoro]

    if len(pelaaja_tiedot['kasi']) > max_kortit and vuoro != 'jakaja':
        print('\n[bold red]Voit ottaa enintään viisi (5) korttia per käsi.[/bold red]')
        return
    
    kortti = hae_satunnainen_kortti(korttipakka)
    pelaaja_tiedot['kasi'].append(kortti)
    peli_tiedot['korttipakka'].remove(kortti)

    pelaajan_kaden_arvo = sum([kasi['arvo'] for kasi in pelaaja_tiedot['kasi']])
    if peli_tiedot['pelimuoto'] == 'kaveri' and pelaajan_kaden_arvo >= 21:
        jää(peli_tiedot['pelimuoto'], peli_tiedot['vuoro'])

    return kortti


def jää(pelimuoto, pelaaja):
    if pelimuoto == 'yksin':
        while True:
            jakajan_kaden_arvo = sum([kortti['arvo'] for kortti in pelaajien_tiedot['jakaja']['kasi']])
            if jakajan_kaden_arvo > 17:
                tarkista_voitto(True)
                peli('yksin')
                break
            else:    
                ota_kortti('jakaja', peli_tiedot['korttipakka'])
                continue
    else:
        peli_vuorot()


def tuplaa(pelaaja):
    pelaajan_tiedot = pelaajien_tiedot[pelaaja]
    pelaajan_panos = pelaajien_tiedot[pelaaja]['panos']
    pelaajan_saldo = pelaajien_tiedot[pelaaja]['saldo'] + pelaajan_panos
  
    if pelaajan_saldo >= pelaajan_panos*2:
        pelaajan_tiedot['panos'] *= 2
        ota_kortti(peli_tiedot['vuoro'], peli_tiedot['korttipakka'])
        jää(peli_tiedot['pelimuoto'], pelaaja)
    else:
        print('Sinulla ei riitä saldo tuplaamiseen')        


def tarkista_voitto(muu_voitto):
    pelaajat = []
    arvot = []
    pelimuoto = peli_tiedot['pelimuoto']

    for pelaaja in pelaajien_tiedot:
        pelaajat.append(pelaaja)
        kaden_arvo = sum([kortti['arvo'] for kortti in pelaajien_tiedot[pelaaja]['kasi']])
        arvot.append(kaden_arvo)

        if pelimuoto == 'yksin':
            if kaden_arvo > 21:
                voittaja = 'Pelaaja' if pelaaja == 'jakaja' else pelaaja
                lisaa_voitto(voittaja)
                poista_panos(voittaja)
                return print(f'\n[bold {"red" if voittaja == "jakaja" else "green"}]{"Hävisit" if voittaja == "jakaja" else "Voitit"} kierroksen[/bold {"red" if voittaja == "jakaja" else "green"}]'), voittaja, 'bust'  
            elif kaden_arvo == 21:
                voittaja = 'jakaja' if pelaaja == 'jakaja' else pelaaja
                lisaa_voitto(voittaja)
                poista_panos(voittaja)
                return print(f'\n[bold {"red" if voittaja == "jakaja" else "green"}]{"Hävisit" if voittaja == "jakaja" else "Voitit"} kierroksen[/bold {"red" if voittaja == "jakaja" else "green"}]'), voittaja, 'blackjack'
    
    if muu_voitto:
        arvot_voitosta = [21-arvo for arvo in arvot]
        lahin = min(arvot_voitosta)
        voittaja_index = arvot_voitosta.index(lahin)
        voittaja = pelaajat[voittaja_index]

        if pelimuoto == 'yksin' and voittaja is 'jakaja':
            poista_panos('Pelaaja')
            return print(f'[bold red]\nHävisit kierroksen[/bold red]'), voittaja
        elif pelimuoto == 'kaveri' and voittaja_index == len(pelaajien_tiedot)-1:
            lisaa_voitto(voittaja)
            poista_panos(voittaja)
            print(f'[bold green]\n{voittaja} voitti kierroksen[/bold green]'), voittaja   
            peli('kaveri')   
        else:
            lisaa_voitto(voittaja)
            poista_panos(voittaja)
            return print(f'[bold green]\n{voittaja} voitti kierroksen[/bold green]'), voittaja

    return 'Jatkuu'

            
def lisaa_voitto(pelaaja):
    pelaajien_tiedot[pelaaja]['saldo'] += pelaajien_tiedot[pelaaja].get('panos', 0) * 2


def poista_panos(pelaaja):
    pelaajien_tiedot[pelaaja].pop('panos', None)


   

def tietokone(saldo):
    print(saldo)

aloita_peli()



