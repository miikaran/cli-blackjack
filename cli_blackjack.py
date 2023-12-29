import random

pelikortit = {
    'maat': ['♠', '♥', '♦', '♣'],
    'arvot': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] 
}

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


print(generoi_korttipakka(pelikortit))



