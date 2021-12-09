# Algoritmo A estrella - Papaya Warehouse
# Fernando Olivares Naranjo
# Diego Sánchez Martín


# ---------------------------------------------------------------------------------------------------------
# Clase Bandeja (los nodos)
# ---------------------------------------------------------------------------------------------------------
class NodoBandeja:
    def __init__(self, peso, precio, lista_papayas):
        self.peso = peso
        self.precio = precio
        self.lista_papayas = lista_papayas
        self.padre = None
        self.g = 0
        self.h = 0

    def f(self):
        return self.g + self.h


# ---------------------------------------------------------------------------------------------------------
# Minimiza f (el precio) y maximiza el peso respecto al límite necesario (2kg)
# ---------------------------------------------------------------------------------------------------------
def nodo_minimiza_f(lista_abiertos):
    nodo_minimo = lista_abiertos[0]
    for nodo in lista_abiertos:
        if nodo.f() < nodo_minimo.f():
            nodo_minimo = nodo
    return nodo_minimo


# ---------------------------------------------------------------------------------------------------------
# Comprobación para obtención de nodo_sig.
# ---------------------------------------------------------------------------------------------------------
def get_nodo(identificador_bandeja_sig, nodos):
    for nodo in nodos:
        if identificador_bandeja_sig in nodo.lista_papayas:
            return nodo
    return None


# ---------------------------------------------------------------------------------------------------------
# Heurística: minimiza precio y se maximiza peso respecto a los 2kg.
# ---------------------------------------------------------------------------------------------------------
def heu(nodo_in, nodo_fi):
    return nodo_fi.precio - nodo_in.precio


def calculo_heuristica(nodo_actual, nodo_sig):
    return heu(nodo_actual, nodo_sig)


# ---------------------------------------------------------------------------------------------------------
# Algoritmo A estrella. Implementación similar a la vista en clase, con salida de éxito ante
# cumplimiento de condiciones de bandeja y peso.
# ---------------------------------------------------------------------------------------------------------
def a_estrella(inicio, fin, nodos):
    lista_abierta = []
    lista_cerrada = []
    nodo_actual = inicio
    nodo_actual.h = heu(inicio, fin)
    lista_abierta.append(inicio)
    while len(lista_abierta) > 0:
        nodo_actual = nodo_minimiza_f(lista_abierta)
        if nodo_actual.peso > fin.peso:
            break
        for bandeja_sig_ID in nodos:
            # nodo_sig = getNodo(bandeja_sig_ID, nodos)
            nodo_sig = bandeja_sig_ID
            papaya_sig_coste_actual = nodo_actual.g + calculo_heuristica(nodo_actual, nodo_sig)
            if nodo_sig in lista_abierta:
                if nodo_sig.g <= papaya_sig_coste_actual:
                    continue
            elif nodo_sig in lista_cerrada:
                if nodo_sig.g <= papaya_sig_coste_actual:
                    continue
                lista_cerrada.remove(nodo_sig)
                lista_abierta.append(nodo_sig)
            else:
                lista_abierta.append(nodo_sig)
                nodo_sig.h = heu(nodo_sig, fin)
            nodo_sig.g = papaya_sig_coste_actual
            nodo_sig.padre = nodo_actual

        lista_abierta.remove(nodo_actual)
        lista_cerrada.append(nodo_actual)

    if nodo_actual.peso < fin.peso:
        return None
    else:
        return nodo_actual


# ---------------------------------------------------------------------------------------------------------
# Clase Papaya.
# ---------------------------------------------------------------------------------------------------------
class Papaya:
    def __init__(self, identificador, peso, dias):
        self.identificador = identificador
        self.peso = peso
        self.dias = dias
