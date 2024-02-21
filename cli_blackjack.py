import random
from rich import print
from rich.console import Console
from kortti import tulosta_kortti
from colorama import init, Back

init(autoreset=True)
pelikortit = {'maat': ['♠', '♥', '♦', '♣'], 'arvot': [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]}
peli_tiedot = {}
pelaajien_tiedot = {}

def menu():
    print()
    console = Console()
    blackjack_tulostus = [
        "[bold magenta]BBBBB[/bold magenta]  [bold magenta]LL[/bold magenta]      [bold magenta]A    [/bold magenta]CCCCC  [bold magenta]K   K  [/bold magenta] JJJJJ  [bold magenta]A    [/bold magenta]CCCCC  [bold magenta]K   K[/bold magenta]",
        "[bold magenta]B   B[/bold magenta]  [bold magenta]LL[/bold magenta]     [bold magenta]A A  [/bold magenta]C       [bold magenta]K  K  [/bold magenta]     J  [bold magenta]A A  [/bold magenta]C       [bold magenta]K  K[/bold magenta]",
        "[bold magenta]BBBBB[/bold magenta]  [bold magenta]LL[/bold magenta]    [bold magenta]AAAAA[/bold magenta] C       [bold magenta]KK    [/bold magenta]     J [bold magenta]AAAAA[/bold magenta] C       [bold magenta]KK[/bold magenta]",
        "[bold magenta]B   B[/bold magenta]  [bold magenta]LL[/bold magenta]    [bold magenta]A   A [/bold magenta]C       [bold magenta]K  K  [/bold magenta] J   J [bold magenta]A   A [/bold magenta]C       [bold magenta]K  K[/bold magenta]",
        "[bold magenta]BBBBB[/bold magenta]  [bold magenta]LLLLL[/bold magenta] [bold magenta]A   A [/bold magenta] CCCCC  [bold magenta]K   K [/bold magenta] JJJJ [bold magenta]A   A [/bold magenta] CCCCC  [bold magenta]K   K[/bold magenta]"
    ]

    for line in blackjack_tulostus:
        console.print(line)
    print('\n[bold red]Tervetuloa pelaamaan komentolinja Blackjackkia! [/bold red]')
    print('[cyan3]Valitse numeroilla pelimuoto, jota haluat pelata.[/cyan3]\n')
    print('1. [bold light_cyan1]Yksin[/bold light_cyan1]\n2. [bold light_cyan1]Kavereita vastaan[/bold light_cyan1]\n3. [bold bright_red]Lopeta peli[/bold bright_red]\n')
    valitse_pelimuoto = ota_kayttajan_input()
    menu_vaihtoehdot = {
        1: 'yksin',
        2: 'kaveri',
        3: 'quit'
    }
    kayttajan_input = menu_vaihtoehdot.get(valitse_pelimuoto, menu)
    if(kayttajan_input == 'quit'):
        quit()
    aloita_peli(kayttajan_input)

def aloita_peli(pelimuoto):
    pelaajien_valmistus(pelimuoto)
    peli(pelimuoto)

def peli(valittu_pelimuoto):
    # Tallennetaan valittu pelimuoto ja ensimmäisen pelaajan vuoro.
    peli_tiedot['pelimuoto'] = valittu_pelimuoto
    peli_tiedot['vuoro'] = list(pelaajien_tiedot.keys())[0]
    # Aloitetaan uusi kierros, asetetaan panos ja jaetaan kädet pelaajille.
    print('\n[bold light_cyan1]Aloitetaan uusi kierros![/bold light_cyan1]')
    aseta_panos()
    jaa_kasi()
    while True:   
        # Tarkista voitto yksinpelissä jokaisen toiminnon jälkeen.
        if valittu_pelimuoto == 'yksin':
            automaattinen_voitto = tarkista_voitto(False)          
            if automaattinen_voitto != 'Jatkuu':
                peli('yksin')
        else: # Muuten näytetään vain tiedot jokaisen pelaajan toiminnon jälkeen.
            nayta_tiedot()
        # Valitaan pelaajan kierroksen toiminto.
        # Jos pelaaja on jakanut kätensä, niin pelaajalla on kummallekkin kädelle oma vuoro.
        if 'kasi1' in pelaajien_tiedot[peli_tiedot['vuoro']].keys():
            jaettu_kasi_handler(pelaajien_tiedot, peli_tiedot)
        else:
            yksittainen_kasi_handler(valittu_pelimuoto, peli_tiedot)

def yksittainen_kasi_handler(pelimuoto, vuoro):
    # Käsitellään yksittäisen käden vaihtoehdot.
    print(f'\n{peli_tiedot["vuoro"]} - Mitä haluat tehdä kädelle?')
    print_kasi_vaihtoehdot()
    vastaus = ota_kayttajan_input()
    kasittele_kayttajan_vaihtoehto(pelimuoto, vastaus, peli_tiedot)

def jaettu_kasi_handler(pelaajien_tiedot, peli_tiedot):
    # Käsitellään jaetun käsien vaihtoehdot.
    for kasi in range(2):
        print(f'\n{peli_tiedot["vuoro"]} - Mitä haluat tehdä kädellä {kasi}?')
        print_kasi_vaihtoehdot()
        vastaus = ota_kayttajan_input()
        kasittele_kayttajan_vaihtoehto(peli_tiedot["vuoro"], vastaus)

def print_kasi_vaihtoehdot():
    print('\n1. Ota kortti\n3. Tuplaus\n4. Jää')

def ota_kayttajan_input():
    try:
        return int(input('=> '))
    except ValueError:
        print('Virheellinen valinta')

def kasittele_kayttajan_vaihtoehto(pelimuoto, vastaus, peli_tiedot):
    match vastaus:
        case 1:
            ota_kortti(peli_tiedot['vuoro'], peli_tiedot['korttipakka'])
        case 3:
            tuplaa(peli_tiedot['vuoro'])
        case 4:
            jää(pelimuoto, peli_tiedot['vuoro'])              
           
def pelaajien_valmistus(valittu_pelimuoto):
    # Alustetaan pelaajien tiedot pelimuodon mukaan.
    match valittu_pelimuoto:
        case 'yksin':
            pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['jakaja'] = {}, {}
        case 'tietokone':
            pelaajien_tiedot['Pelaaja'], pelaajien_tiedot['tietokone'] = {}, {}
        case 'kaveri':
            print('\n[bold red]Lisätään pelaajia peliin.[/bold red]')
            pelaaja_jarjestys = 1 

            while True: # Lisätään pelaajia moninpelissä.
                print('[cyan3]Kirjoita S tallentaaksesi lisäyksesi[/cyan3]\n')
                nimi = input(f'\n{pelaaja_jarjestys}. pelaajan nimi: ')

                # Tallennetaan lisätyt pelaajat "S" kirjaimella.
                if nimi.lower() == 's':
                    if len(pelaajien_tiedot) > 0:
                        print('Tallennetaanko pelaajat?')
                        for pelaaja in pelaajien_tiedot:
                            print(pelaaja)
                        varmistus = input('Kylla/Ei? => ').lower()
                        if varmistus == 'kylla':
                            break
                        else:
                            continue
                    break
                if nimi == None or nimi == '':
                    print('[bold red]Älä jätä pelaajan nimeä tyhjäksi[/bold red]\n')
                    continue
                else:
                    # Lisätään pelaaja pelaajien_tiedot objektiin.
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
    #Asetetaan pelaajien panokset
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
    # Näytetään pelaajien tiedot (panos, saldo, kasi, jne).
    for pelaaja in pelaajien_tiedot:
        tiedot = pelaajien_tiedot[pelaaja]
        if pelaaja != 'jakaja':
            try:
                print('\n===========================================')
                pelaajan_saldo = tiedot['saldo'] + tiedot['panos']
                print(f'{pelaaja}n saldo: {pelaajan_saldo}$')
                print(f'{pelaaja}n panos: {tiedot['panos']}$')
                print(f"{pelaaja}n kasi:", end=" ")
                for kortti in tiedot['kasi']:
                    tulosta_kortti(kortti['arvo'], kortti['maa'])
                print('\n===========================================')
            except KeyError:
                pass
        else:
            try: # Näytetään jakajan käsi erikseen, mikäli pelataan yksinpeliä.
                print('\n===========================================')
                print(f'Jakajan käsi:', end=" ")
                for kortti in tiedot['kasi']:
                    tulosta_kortti(kortti['arvo'], kortti['maa'])
                print('\n===========================================')
            except KeyError:
                pass
    
def peli_vuorot():
    # Tämä funktio hallitsee pelin vuorot moninpelissä.
    print(peli_tiedot['vuoro'])
    pelaajat = list(pelaajien_tiedot.keys())
    vuoro_index = pelaajat.index(peli_tiedot['vuoro'])
    seuraava = vuoro_index+1
    # Kun viimeinen pelaaja on tehnyt tehnyt valinnan, niin tarkistetaan voitto.
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
    # Jaetaan pelikäsi jokaiselle pelaajalle.
    for pelaaja in pelaajien_tiedot:
        pelaajan_tiedot = pelaajien_tiedot[pelaaja]
        kasi = [hae_satunnainen_kortti(korttipakka) for _ in range(2)]
        pelaajan_tiedot['kasi'] = kasi

def ota_kortti(vuoro, korttipakka):
    max_kortit = 4
    pelaaja_tiedot = pelaajien_tiedot[vuoro]    
    # Kortin ottaminen (hit) voi tehdä maksimissaan viiteen korttiin asti.
    if len(pelaaja_tiedot['kasi']) > max_kortit and vuoro != 'jakaja':
        print('\n[bold red]Voit ottaa enintään viisi (5) korttia per käsi.[/bold red]')
        return
    kortti = hae_satunnainen_kortti(korttipakka)
    pelaaja_tiedot['kasi'].append(kortti)
    peli_tiedot['korttipakka'].remove(kortti)
    pelaajan_kaden_arvo = sum([kasi['arvo'] for kasi in pelaaja_tiedot['kasi']])
    # Jos moninpelissä kortin ottamisen jälkeen pelaajan käden arvo on yli 21 hän jää automaattisesti.
    if peli_tiedot['pelimuoto'] == 'kaveri' and pelaajan_kaden_arvo >= 21:
        jää(peli_tiedot['pelimuoto'], peli_tiedot['vuoro'])

    return kortti

def jää(pelimuoto, pelaaja):
    #pelaajan_tiedot = pelaajien_tiedot['vuoro']
    if pelimuoto == 'yksin':
        while True: # Yksinpelissä jakaja nostaa sääntöjen mukaisesti kortteja siihen asti, kunnes käden arvo on 17 tai yli.
            jakajan_kaden_arvo = sum([kortti['arvo'] for kortti in pelaajien_tiedot['jakaja']['kasi']])
            if jakajan_kaden_arvo > 17:
                # Kun jakajan kaden arvo on yli 17 tarkistetaan voitto ja aloitetaan uusi kierros
                tarkista_voitto(True)
                peli('yksin')
            else:    
                ota_kortti('jakaja', peli_tiedot['korttipakka'])
                continue
    else:
        # Jos pelimuoto ei ole yksinpeli, niin voitto tarkistetaan viimeisen pelaajan jälkeen.
        peli_vuorot()

def tuplaa(pelaaja):
    pelaajan_tiedot = pelaajien_tiedot[pelaaja]
    pelaajan_panos = pelaajien_tiedot[pelaaja]['panos']
    pelaajan_saldo = pelaajien_tiedot[pelaaja]['saldo'] + pelaajan_panos
    # Jos pelaaja tuplaa, niin hän ottaa automaattisesti yhden kortin, jonka jälkeen vuoro siirtyy eteenpäin.
    if pelaajan_saldo >= pelaajan_panos*2:
        pelaajan_tiedot['panos'] *= 2
        ota_kortti(peli_tiedot['vuoro'], peli_tiedot['korttipakka'])
        if peli_tiedot['pelimuoto'] == 'yksin':
            jää('yksin', peli_tiedot['vuoro'])
    else:
        print('Sinulla ei riitä saldo tuplaamiseen')    

def jako(pelaaja):
    pelaajan_tiedot = pelaajien_tiedot[pelaaja]
    # Jaetaan pelaajan käsi kahteen erilliseen käteen.
    if pelaajan_tiedot['kasi'][0]['arvo'] == pelaajan_tiedot['kasi'][1]['arvo'] and len(pelaajan_tiedot['kasi']) == 2:
        pelaajan_tiedot['kasi1'] = [pelaajan_tiedot['kasi'][1]]
        pelaajan_tiedot['kasi'] = [pelaajan_tiedot['kasi'][0]]
        # Haetaan kummallekkin kädelle uusi kortti.
        for kasi in range(2):
            if kasi == 0:
                pelaajan_tiedot['kasi'].append(hae_satunnainen_kortti(peli_tiedot['korttipakka']))
            else:
                pelaajan_tiedot[f'kasi{kasi}'].append(hae_satunnainen_kortti(peli_tiedot['korttipakka']))
    else:
        print('Et pysty jakamaan kädelläsi')
    
def tarkista_voitto(muu_voitto):
    '''
    Tätä funktiota käytetään voiton tarkistukseen kaikissa pelimuodoissa.
    Yksinpelin automaattisen voiton tarkistamiseen on funktion sisällä luotu omat ehtolausekkeet. 
    '''
    pelaajat_arvot = []
    pelimuoto = 'kaveri' if peli_tiedot['pelimuoto'] != 'tietokone' and peli_tiedot['pelimuoto'] != 'yksin' else peli_tiedot['pelimuoto']
    voittaja = ''
    nayta_tiedot()

    for pelaaja in pelaajien_tiedot:
        kaden_arvo = sum([kortti['arvo'] for kortti in pelaajien_tiedot[pelaaja]['kasi']])
        pelaajat_arvot.append({'pelaaja': pelaaja, 'arvo': kaden_arvo})
    
        if pelimuoto == 'yksin':
            if kaden_arvo > 21:
                voittaja = 'Pelaaja' if pelaaja == 'jakaja' else 'jakaja'
                lisaa_voitto(voittaja, False)
                poista_panos()
                return print(f'\n[bold {"red" if voittaja == "jakaja" else "green"}]{"Hävisit" if voittaja == "jakaja" else "Voitit"} kierroksen[/bold {"red" if voittaja == "jakaja" else "green"}]'), voittaja, 'bust'  
            elif kaden_arvo == 21:
                voittaja = 'jakaja' if pelaaja == 'jakaja' else pelaaja
                lisaa_voitto(voittaja, False)
                poista_panos()
                return print(f'\n[bold {"red" if voittaja == "jakaja" else "green"}]{"Hävisit" if voittaja == "jakaja" else "Voitit"} kierroksen[/bold {"red" if voittaja == "jakaja" else "green"}]'), voittaja, 'blackjack'
    if muu_voitto:
        # Järjestetään pelaajien käsien arvot.
        voitto_jarjestys = sorted(pelaajat_arvot, key=lambda x: x['arvo'])
        saman_arvoiset_kadet = []
        # Määritetään voittaja
        for pelaaja in voitto_jarjestys:
            if pelaaja['arvo'] <= 21:
                for kasi in voitto_jarjestys:
                    if pelaaja['arvo'] == kasi['arvo'] and pelaaja['pelaaja'] != kasi['pelaaja']:
                        if len(saman_arvoiset_kadet) > 1:
                            saman_arvoiset_kadet = []
                        saman_arvoiset_kadet.append(kasi)
                voittaja = pelaaja['pelaaja']
            else:
                break 
        # Jos pelaajilla on samanarvoiset kädet, niin tulee tasapeli.
        if len(saman_arvoiset_kadet) != 0:
            tasapeli_pelaajat = ''
            for pelaajat in saman_arvoiset_kadet:
                tasapeli_pelaajat += pelaajat['pelaaja'] + ' & ' if pelaajat != saman_arvoiset_kadet[len(saman_arvoiset_kadet)-1] else pelaajat['pelaaja']
            print(f'[bold light_cyan1]\n{tasapeli_pelaajat} teillä tuli tasapeli![/bold light_cyan1]'), voittaja
            lisaa_voitto(saman_arvoiset_kadet, True)  
        elif pelimuoto == 'yksin' and voittaja == 'jakaja':
            print(f'[bold red]\nHävisit kierroksen[/bold red]'), voittaja
        elif pelimuoto == 'kaveri' and len(pelaajat_arvot) == len(pelaajien_tiedot):
            lisaa_voitto(voittaja, False)
            print(f'[bold green]\n{voittaja} voitti kierroksen[/bold green]'), voittaja    
        else:
            lisaa_voitto(voittaja, False)
            print(f'[bold green]\n{voittaja} voitti kierroksen[/bold green]'), voittaja      
        poista_panos()
        peli(pelimuoto)
    return 'Jatkuu'
         
def lisaa_voitto(pelaaja, tasapeli):
    # Voiton lisäykset voittajille.
    if tasapeli:
        for p in pelaaja:
            try:
                pelaajien_tiedot[p['pelaaja']]['saldo'] += pelaajien_tiedot[p['pelaaja']].get('panos', 0) * 1
            except:
                pass
    else:
        try:
            pelaajien_tiedot[pelaaja]['saldo'] += pelaajien_tiedot[pelaaja].get('panos', 0) * 2
        except:
            pass

def poista_panos():
    # Panosten poistamisen kierroksen jälkeen.
    for pelaaja in pelaajien_tiedot:
        try:
            pelaajien_tiedot[pelaaja].pop('panos', None)
        except:
            pass


def tietokone(saldo):
    print(saldo)

menu()



