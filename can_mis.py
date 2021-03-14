import math
import os
import sys
import time

class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, fisier):
        l = self.obtineDrum()
        for index, nod in enumerate(l):
            fisier.write(str(index + 1) + ' ' + str(nod) + '\n')
        fisier.write("Cost: " + str(self.g) + '\n')
        fisier.write("Lungimea drumului: " + str(len(l)) + '\n\n\n')
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info) + "\n"
        return sir

    def __str__(self):
        '''
        sir = str(self.info)
        return sir
        '''
        if self.info[3] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
            malSt = "vest"
            malDr = "est"
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"
            malSt = "est"
            malDr = "vest"
        return (
                    "Mal: " + Graph.malInit + " Copii: {} Misionari: {} Canibali {} {}  |||  Mal:" + Graph.malFin + " Copii: {} Misionari: {} Canibali: {} {} \nBarca pleaca de pe malul de " + str(malSt) + " catre malul de " + str(malDr)+"\n").format(
            self.info[0], self.info[1], self.info[2], barcaMalInitial, Graph.COP - self.info[0], Graph.MIS - self.info[1], Graph.CAN - self.info[2], barcaMalFinal)
        # afisarea in formatul dorit in cerinta


class Graph:
    def __init__(self, cale):
        f = open(cale, "r")
        continutFisier = f.readlines()
        infoProblema = [int(continutFisier[i].split("=")[1]) for i in range(0, 3)]
        locuri = int(continutFisier[3].split("=")[1])
        malInit = 1 if 'vest' == continutFisier[4].split("=")[1].strip() else 0
        malFin = 0 if 'est' == continutFisier[5].split("=")[1].strip() else 1

        [Graph.COP, Graph.MIS, Graph.CAN] = infoProblema
        Graph.LOC = locuri
        Graph.malInit = continutFisier[4].split("=")[1].strip()
        Graph.malFin = continutFisier[5].split("=")[1].strip()
        potPleca = Graph.COP
        self.start = (Graph.COP, Graph.MIS, Graph.CAN, malInit, potPleca)
        self.scopuri = [(0, 0, 0, 0)]
        self.nrNoduri = 20

    def genereazaSuccesori(self, nodCurent, tip_euristica=""):
        '''
        Conditii:
        1. copiii sa nu ramana singuri sau doar cu canibalii
        2. numarul de misionari + numarul de copii / 2 sa fie mai mare decat numarul de canibali (din cerinta)
        3. numarul de copii, canibali si misionari sa nu fie mai mic de 0
        '''
        def conditie(cop, mis, can):
            return (cop != 0 and can == 0 and mis == 0) or (cop != 0 and mis == 0 and can != 0) or ((mis+cop/2) < can) or (can < 0 or mis < 0 or cop < 0)

        listaSuccesori = []
        (copMalInitial, misMalInitial, canMalInitial, barca, potPleca) = nodCurent.info
        '''
        Preluarea oamenilor de pe cele doua maluri
        '''
        if barca == 1 :
            canMalCurent = canMalInitial
            misMalCurent = misMalInitial
            copMalCurent = copMalInitial

            canMalOpus = Graph.CAN - canMalCurent
            misMalOpus = Graph.MIS - misMalCurent
            copMalOpus = Graph.COP - copMalCurent
        else:
            canMalOpus = canMalInitial
            misMalOpus = misMalInitial
            copMalOpus = copMalInitial

            canMalCurent = Graph.CAN - canMalOpus
            misMalCurent = Graph.MIS - misMalOpus
            copMalCurent = Graph.COP - copMalOpus

        ''' 
        Incarcarea in barca a oamenilor
        '''
        maxCopBarca = min(Graph.LOC-1, copMalCurent)  # Graph.LOC-1 intrucat in cazul in care urc un copil in barca
                                                      # acesta trebuie insotit de macar un misionar
        for copBarca in range(maxCopBarca + 1):
            if copBarca == 0:
                maxMisBarca = min(Graph.LOC, misMalCurent)
                minMisBarca = 0  # daca numarul de copii este 0, numarul minim de misionari este tot 0

            elif copBarca > potPleca:  # conditia cu raul de mare - pe ultima pozitie din fiecare nod retin cati copii
                                       # pot pleca (intrucat copiii care tocmai au ajuns pe un mal nu pot pleca imediat
                                       # dupa
                continue

            else:
                maxMisBarca = min(Graph.LOC - copBarca, misMalCurent)
                minMisBarca = 1  # daca numarul de copii este macar 1, atunci ei trebuie insotiti de macar un misionar (ca sa respecte cerinta)

            for misBarca in range(minMisBarca, maxMisBarca + 1):
                if misBarca == 0:
                    maxCanBarca = min(Graph.LOC, canMalCurent)
                    minCanBarca = 1  # daca numarul de misionari este 0 (deci implicit si numarul de copii este 0, numarul de canibali trebuie sa fie macar 1
                                     # intrucat barca nu se poate deplasa goala
                else:
                    maxCanBarca = min(Graph.LOC - misBarca - copBarca, canMalCurent, math.floor(misBarca + copBarca / 2))
                    minCanBarca = 0  # in cazul in care exista deja copii si/sau misionari urcati in barca, numarul de canibali poate fi si 0
                                     # deoarece se respecta deja conditia ca barca sa nu fie goala pentru a se putea deplasa

                for canBarca in range(minCanBarca, maxCanBarca + 1):
                    '''
                    Updatarea numarului de persoane de pe cele doua maluri
                    De pe malul curent scad persoanele care pleaca
                    De pe malul opus adaug persoanele care sosesc
                    '''
                    canMalCurentNou = canMalCurent - canBarca
                    misMalCurentNou = misMalCurent - misBarca
                    copMalCurentNou = copMalCurent - copBarca

                    canMalOpusNou = canMalOpus + canBarca
                    misMalOpusNou = misMalOpus + misBarca
                    copMalOpusNou = copMalOpus + copBarca

                    if conditie(copMalCurentNou, misMalCurentNou, canMalCurentNou): #daca nu respecta cerintele, sar peste
                        continue
                    if conditie(copMalOpusNou, misMalOpusNou, canMalOpusNou):
                        continue

                    if barca == 1:
                        infoNod = (copMalCurentNou, misMalCurentNou, canMalCurentNou, 0, copMalOpusNou - copBarca)  # copMalOpusNou - copBarca este necesar pentru a respecta
                                                                                                                    # conditia ca acei copii care tocmai au ajuns sa nu poata
                                                                                                                    # pleca imediat dupa
                    else:
                        infoNod = (copMalOpusNou, misMalOpusNou, canMalOpusNou, 1, copMalOpusNou - copBarca)

                    if not nodCurent.contineInDrum(infoNod):
                        listaSuccesori.append(NodParcurgere(infoNod, nodCurent, nodCurent.g + 1 + copBarca, h=self.calculeaza_h(infoNod, tip_euristica)))
                        # adaugarea nodului nou creat in lista de succesori

        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica=""):
        if tip_euristica == "euristica_admisibila_1":
            return 2 * math.ceil((infoNod[0]+infoNod[1]+infoNod[2]) / self.LOC) + (1-infoNod[3]) - 1

            # numarul minim de drumuri care poate fi efectuat, presupunand ca barca este mereu plina atunci cand
            # face cele doua drumuri. Inmultesc cu 2 intrucat barca trebuie sa se si intoarca, iar la final scad
            # maxim un 1 (deoarece barca se poate afla pe oricare din cele doua maluri intr un oarecare moment)

        if tip_euristica == "euristica_admisibila_2":
            return 2 * math.ceil((infoNod[0]+infoNod[1]+infoNod[2]) / self.LOC) + (1-infoNod[3]) - 1 + infoNod[0]

            # am ales aceeasi euristica ca inainte, la care am adaugat inca o valoare care sa depinda de starea actuala
            # si anume numarul de copii, intrucat aceasta ofera o estimare mai buna

        if tip_euristica == "euristica_neadmisibila":
            return 3 * infoNod[0] + 5 * infoNod[1] + 7 * infoNod[2]

            # reprezinta o serie de inmultiri pentru a ma asigura ca acest numar este prea mare pentru a fi bun

        return 0

    def testeaza_scop(self, nodCurent):
        return nodCurent.info[0:4] == (0, 0, 0, 0)
        # verific ca primele 4 valori din nod sa fie 0
        # in nod am 5 valori, insa pe ultima pozitie se afla numarul de copii care pot pleca imediat, care este irelevant
        # atunci cand testez daca o anumita stare este finala

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def breadth_first(gr, fisier, nrSolutii):
    t1 = time.time()
    fis = open(fisier, 'w+')
    fis.write("BF"+ '\n')
    fis.write("====================================" + '\n')
    c = [NodParcurgere(gr.start, None)]
    continua = True
    nrNoduri = 0
    while len(c) > 0 and continua:
        if time.time() - t1 > float(timeout):
            print("Timeout pentru breadth first!")
            break
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            fis.write("Solutie: " + '\n')
            nodCurent.afisDrum(fis)
            fis.write("=======================\n")
            nrSolutii -= 1
            if nrSolutii == 0:
                continua = False
        listaSuccesori = gr.genereazaSuccesori(nodCurent)
        nrNoduri += len(listaSuccesori)
        c.extend(listaSuccesori)

    fis.write("Numarul de noduri: " + str(nrNoduri))

nr_Noduri_df = 0
def depth_first(gr, fisier, nrSolutiiCautate=1):
    global nr_Noduri_df
    nr_Noduri_df = 0
    fis = open(fisier, 'w+')
    fis.write("DF" + '\n')
    fis.write("====================================" + '\n')
    df(NodParcurgere(gr.start, None), fis, nrSolutiiCautate, time.time())


def df(nodCurent, fis, nrSolutiiCautate, t1):
    global nr_Noduri_df
    if time.time() - t1 > float(timeout):
        print("Timeout pentru depth first!")
        return
    if nrSolutiiCautate == 0:
        return nrSolutiiCautate


    if gr.testeaza_scop(nodCurent):
        fis.write("Solutie: " + '\n')
        nodCurent.afisDrum(fis)
        fis.write("=======================\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            fis.write("Numarul de noduri: " + str(nr_Noduri_df))
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    nr_Noduri_df += len(lSuccesori)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(sc, fis, nrSolutiiCautate, t1)
    return nrSolutiiCautate


def dfi(nodCurent, adancime, fis, nrSolutiiCautate, t1):
    if time.time() - t1 > float(timeout):
        print("Timeout pentru depth first iterativ!")
        return
    global nr_Noduri
    if adancime == 1 and gr.testeaza_scop(nodCurent):
        fis.write("Solutie: " + '\n')
        nodCurent.afisDrum(fis)
        fis.write("=======================\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            fis.write("Numarul de noduri: " + str(nr_Noduri))
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        nr_Noduri += len(lSuccesori)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(sc, adancime - 1, fis, nrSolutiiCautate, t1)

    return nrSolutiiCautate

nr_Noduri = 0
def depth_first_iterativ(gr, fisier, nrSolutiiCautate = 1):
    global nr_Noduri
    nr_Noduri = 0
    fis = open(fisier, 'w+')
    fis.write("DFI" + '\n')
    fis.write("====================================" + '\n')
    for i in range(1, gr.nrNoduri + 1):
        if nrSolutiiCautate == 0:
            return
        #print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(NodParcurgere(gr.start, None), i, fis, nrSolutiiCautate, time.time())


def uniform_cost(gr, fisier, nrSolutiiCautate=1):
    t1 = time.time()

    fis = open(fisier, 'w+')
    fis.write("UCS" + '\n')
    fis.write("====================================" + '\n')
    c = [NodParcurgere(gr.start, None, 0)]
    nrNoduri = 0
    while len(c) > 0:
        if float(time.time() - t1) > float(timeout):
            print("Timeout pentru UCS!")
            break

        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            fis.write("Solutie: " + '\n')
            nodCurent.afisDrum(fis)
            fis.write("=======================\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                fis.write("Numarul de noduri: " + str(nrNoduri))
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        nrNoduri += len(lSuccesori)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g > s.g:  # la UCS ordonez dupa cost
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, fisier, nrSolutiiCautate, tip_euristica):
    t1 = time.time()
    fis = open(fisier, 'w+')
    fis.write("A* " + tip_euristica +'\n')
    fis.write("====================================" + '\n')
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    nrNoduri = 0
    while len(c) > 0:
        if time.time() - t1 > float(timeout):
            print("Timeout pentru A* la", tip_euristica, "!")
            break
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            fis.write("Solutie: " + '\n')
            nodCurent.afisDrum(fis)
            fis.write("=======================\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                fis.write("Numarul de noduri: " + str(nrNoduri))
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        nrNoduri += len(lSuccesori)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f >= s.f:  # la A* ordonez dupa f (cost + euristica)
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def greedy(gr, fisier, nrSolutiiCautate, tip_euristica):
    t1 = time.time()
    fis = open(fisier, 'w+')
    fis.write("Greedy " + tip_euristica +'\n')
    fis.write("====================================" + '\n')
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    nrNoduri = 0

    while len(c) > 0:
        if time.time() - t1 > float(timeout):
            print("Timeout pentru greedy!")
            break
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            fis.write("Solutie: " + '\n')
            nodCurent.afisDrum(fis)
            fis.write("=======================\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                fis.write("Numarul de noduri: " + str(nrNoduri))
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        nrNoduri += len(lSuccesori)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].h >= s.h:  # la Greedy ordonez dupa euristica
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def nu_exista_solutie(cop, mis, can, loc):
    '''
    Daca avem cel putin un copil si un misionar, iar in barca este un singur loc, starea initiala nu va avea
    nicio solutie, din cauza faptului ca pentru a se deplasa, un copil trebuie mereu sa fie insotit de un misionar

    De asemenea, daca avem copii insa nu avem misionari, acest input nu are solutie intrucat nu respecta regulile
    mentionate in cerinte (i.e. un copil nu se poate afla pe mal sau in barca fara a fi insotit de minim un misionar).
    In acest caz numarul de canibal si locurile in barca sunt irelevante, intrucat solutia nu exista oricum.
    '''

    if cop != 0 and mis != 0 and loc < 2:
        return True
    if cop != 0 and mis == 0:
        return True
    return False


'''
Fisierul 1.txt contine un input care nu are solutii.
Fisierul 2.txt contine un input care e si stare finala.
Fisierul 3.txt contine un input care functioneaza pe toti algoritmii.
Fisierul 4.txt contine un input care se blocheaza pe UCS.
'''

inputdir = sys.argv[1]
outputdir = sys.argv[2]
nrsol = sys.argv[3]
timeout = sys.argv[4]


'''
listaFisiereInput = os.listdir(inputdir)
if not os.path.exists("output"):
    os.mkdir("output")

for numeFisier in listaFisiereInput:
    numeFisierOutput = "output_" + numeFisier
    print(numeFisierOutput)
'''


for nr in range(1, 5):
    fis = inputdir + "/" + str(nr) + ".txt"
    gr = Graph(fis)

    if nu_exista_solutie(gr.COP, gr.MIS, gr.CAN, gr.LOC):
        print("Fisierul " + str(nr) + " contine o stare initiala care nu are solutii.")
        continue

    if gr.malInit == gr.malFin:
        print("Fisierul " + str(nr) + " contine o stare initiala care este deja si stare finala.")
        continue

    print("Fisierul", nr, "...")
    t1 = time.time()
    breadth_first(gr, outputdir + "/" + str(nr) + "_output_bf.txt", int(nrsol))
    f = open(outputdir + "/" + str(nr) + "_output_bf.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1)*1000))

    t1 = time.time()
    depth_first(gr, outputdir + "/" + str(nr) + "_output_df.txt", int(nrsol))
    f = open(outputdir + "/" + str(nr) + "_output_df.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    depth_first_iterativ(gr, outputdir + "/" + str(nr) + "_output_dfi.txt", int(nrsol))
    f = open(outputdir + "/" + str(nr) + "_output_dfi.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    uniform_cost(gr, outputdir + "/" + str(nr) + "_output_ucs.txt", int(nrsol))
    f = open(outputdir + "/" + str(nr) + "_output_ucs.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    a_star(gr, outputdir + "/" + str(nr) + "_output_astar_ea1.txt", int(nrsol), "euristica_admisibila_1")
    f = open(outputdir + "/" + str(nr) + "_output_astar_ea1.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    a_star(gr, outputdir + "/" + str(nr) + "_output_astar_ea2.txt", int(nrsol), "euristica_admisibila_2")
    f = open(outputdir + "/" + str(nr) + "_output_astar_ea2.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    a_star(gr, outputdir + "/" + str(nr) + "_output_astar_en.txt", int(nrsol), "euristica_neadmisibila")
    f = open(outputdir + "/" + str(nr) + "_output_astar_en.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    greedy(gr, outputdir + "/" + str(nr) + "_output_greedy_ea1.txt", int(nrsol), "euristica_admisibila_1")
    f = open(outputdir + "/" + str(nr) + "_output_greedy_ea1.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    greedy(gr, outputdir + "/" + str(nr) + "_output_greedy_ea2.txt", int(nrsol), "euristica_admisibila_2")
    f = open(outputdir + "/" + str(nr) + "_output_greedy_ea2.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

    t1 = time.time()
    greedy(gr, outputdir + "/" + str(nr) + "_output_greedy_en.txt", int(nrsol), "euristica_neadmisibila")
    f = open(outputdir + "/" + str(nr) + "_output_greedy_en.txt", "a")
    f.write('\nTimpul: ' + str((time.time() - t1) * 1000))

