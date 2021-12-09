# Fernando Olivares Naranjo

DEBUG = False

def heu(nodo_in, nodo_fi):
    return -(nodo_fi.precio - nodo_in.precio)


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


def nodo_minimiza_f(lista_abiertos):
    nodo_minimo = lista_abiertos[0]
    for nodo in lista_abiertos:
        if nodo.f() < nodo_minimo.f():
            nodo_minimo = nodo
    return nodo_minimo


def getNodo(identificador_bandeja_sig, nodos):
    for nodo in nodos:
        if identificador_bandeja_sig in nodo.lista_papayas:
            return nodo
    return None


def calculoHeu(nodo_actual, nodo_sig):
    return heu(nodo_actual, nodo_sig)


def a_estrella(inicio, fin, nodos):
    open_list = []
    close_list = []
    nodo_actual = inicio
    nodo_actual.h = heu(inicio, fin)
    open_list.append(inicio)
    while len(open_list) > 0:
        nodo_actual = nodo_minimiza_f(open_list)
        if nodo_actual.peso > 2:
            break
        for bandeja_sig_ID in nodos:
            #nodo_sig = getNodo(bandeja_sig_ID, nodos)
            nodo_sig = bandeja_sig_ID
            papaya_sig_coste_actual = nodo_actual.g + calculoHeu(nodo_actual, nodo_sig)
            #papaya_sig_coste_actual = nodo_actual.g + calculoHeu(nodo_actual, nodo_sig)
            if nodo_sig in open_list:
                if nodo_sig.g <= papaya_sig_coste_actual:
                    continue
            elif nodo_sig in close_list:
                if nodo_sig.g <= papaya_sig_coste_actual:
                    continue
                close_list.remove(nodo_sig)
                open_list.append(nodo_sig)
            else:
                open_list.append(nodo_sig)
                nodo_sig.h = heu(nodo_sig, fin)
            nodo_sig.g = papaya_sig_coste_actual
            nodo_sig.padre = nodo_actual
        open_list.remove(nodo_actual)
        close_list.append(nodo_actual)

    if nodo_actual.peso < fin.peso:
        return None
    else:
        return nodo_actual
        # path = []
        # while nodo_actual is not None:
        #    path.append(nodo_actual)
        #    nodo_actual = nodo_actual.padre
        # return path


class Papaya:
    def __init__(self, identificador, peso, dias):
        self.identificador = identificador
        self.peso = peso
        self.dias = dias


def debug(msg):
    if DEBUG:
        print(msg)
    else:
        pass
