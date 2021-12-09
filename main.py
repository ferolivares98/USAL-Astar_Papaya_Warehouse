# Algoritmo A estrella - Papaya Warehouse
# Fernando Olivares Naranjo
# Diego Sánchez Martín

from Aestrella import *

lista_papayas = [
    Papaya(identificador="1400001", peso=0.273, dias=1.1),
    Papaya(identificador="1400002", peso=0.405, dias=1),
    Papaya(identificador="1400003", peso=0.517, dias=1.1),
    Papaya(identificador="1400004", peso=0.533, dias=1.7),
    Papaya(identificador="1400005", peso=0.358, dias=1.5),
    Papaya(identificador="1400006", peso=0.562, dias=1.9),
    Papaya(identificador="1400007", peso=0.322, dias=2.4),
    Papaya(identificador="1400008", peso=0.494, dias=1.8),
    Papaya(identificador="1400009", peso=0.39, dias=1.6),
    Papaya(identificador="1400010", peso=0.281, dias=2.2),
    Papaya(identificador="1400011", peso=0.395, dias=2),
    Papaya(identificador="1400012", peso=0.407, dias=2),
    Papaya(identificador="1400013", peso=0.329, dias=3),
    Papaya(identificador="1400014", peso=0.629, dias=2.7),
    Papaya(identificador="1400015", peso=0.417, dias=1.2),
    Papaya(identificador="1400016", peso=0.278, dias=1.4),
    Papaya(identificador="1400017", peso=0.583, dias=2.2),
    Papaya(identificador="1400018", peso=0.598, dias=1.9),
    Papaya(identificador="1400019", peso=0.271, dias=1.6),
    Papaya(identificador="1400020", peso=0.265, dias=2.1),
]
num_bandeja = 0


def main():
    papayas = lista_papayas
    peso_total = 0

    print("Calculando...")
    print()

    for p in papayas:
        peso_total = peso_total + p.peso

    while peso_total >= 2:
        copia_papayas = papayas.copy()
        lista_bandejas = []
        bandeja_validada = calculo_bandeja(lista_bandejas, papayas, copia_papayas)
        nueva_papayas = []
        if bandeja_validada:
            print(bandeja_validada.lista_papayas)
            print()
            for p in papayas:
                if p.identificador not in bandeja_validada.lista_papayas:
                    nueva_papayas.append(p)
        papayas = nueva_papayas
        peso_total = 0
        for p in papayas:
            peso_total = peso_total + p.peso

    print("Papayas sobrantes: ")
    for p in papayas:
        print(p.identificador + " | Peso: " + str(p.peso))


# ---------------------------------------------------------------------------------------------------------
# Cálculo de las primeras bandejas por papaya a nivel individual.
# En la bandeja se incluye el precio de la bandeja (suma de papayas) + el de la papaya (COBOT incluido)
# No se incluye el sellado.
# ---------------------------------------------------------------------------------------------------------
def calculo_bandeja(lista_bandejas, papayas, copia_papayas):
    for papaya in papayas:
        bandeja = NodoBandeja(papaya.peso, papaya.peso * 2 + papaya.dias * 0.05 + 0.10, [papaya.identificador])
        lista_bandejas.append(bandeja)
        lista_bandejas_temp = [bandeja]
        for papayaextra in copia_papayas:
            if papayas.index(papayaextra) > papayas.index(papaya):
                if papayaextra.identificador not in bandeja.lista_papayas:  # Si existe [1,2], evitar [2,1]
                    bandeja_extra = NodoBandeja(bandeja.peso + papayaextra.peso,
                                                bandeja.precio + papayaextra.peso * 2 + papaya.dias * 0.05 + 0.10,
                                                bandeja.lista_papayas + [papayaextra.identificador])
                    lista_bandejas_temp.append(bandeja_extra)
        bucle_ampliacion_bandeja(papaya, copia_papayas, lista_bandejas_temp)
        lista_bandejas = lista_bandejas + lista_bandejas_temp

    bandeja_correcta = a_estrella(inicio=lista_bandejas[0], fin=NodoBandeja(2, 0, []), nodos=lista_bandejas)
    if bandeja_correcta.peso > 2:
        global num_bandeja
        num_bandeja += 1
        print("Bandeja Nº: " + str(num_bandeja))
        print("Peso: " + str(bandeja_correcta.peso))
        bandeja_correcta.precio = bandeja_correcta.precio + 0.30  # Sellado de la bandeja
        print("Precio: " + str(bandeja_correcta.precio))
        return bandeja_correcta
    else:
        return None


# ---------------------------------------------------------------------------------------------------------
# Ampliación del tamaño de las bandejas para las búsquedas A*
# De nuevo, intentando eviat repeticiones en las combinaciones.
# ---------------------------------------------------------------------------------------------------------
def bucle_ampliacion_bandeja(papaya, copia_papayas, lista_bandejas):
    for bandeja in lista_bandejas:
        for papayaextra in copia_papayas:
            if len(bandeja.lista_papayas) > 5:
                break
            if int(papayaextra.identificador) > int(bandeja.lista_papayas[-1]):  # De nuevo, evitar repetición.
                if papayaextra.identificador not in bandeja.lista_papayas:
                    bandeja_extra = NodoBandeja(bandeja.peso + papayaextra.peso,
                                                bandeja.precio + papayaextra.peso * 2 + papaya.dias * 0.05 + 0.10,
                                                bandeja.lista_papayas + [papayaextra.identificador])
                    lista_bandejas.append(bandeja_extra)


if __name__ == '__main__':
    main()
