#encoding: utf-8

import time
from Client import SocketClient
import json
import numpy as np

koord = [[-5, 0], [-4, -3], [-4, -2], [-4, -1], [-4, 0], [-4, 1], [-4, 2], [-4, 3], [-3, -4], [-3, -3], [-3, -2], [-3, -1], [-3, 0], [-3, 1], [-3, 2], [-3, 3], [-3, 4], [-2, -4], [-2, -3], [-2, -2], [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3], [-2, 4], [-1, -4], [-1, -3], [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3], [-1, 4], [0, -5], [0, -4], [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, -4], [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, -4], [2, -3], [2, -2], [2, -1], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, -4], [3, -3], [3, -2], [3, -1], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, -3], [4, -2], [4, -1], [4, 0], [4, 1], [4, 2], [4, 3], [5, 0]]


# NaiveHunter stratégia implementációja távoli eléréshez.
class RemoteNaiveHunterStrategy:

    def __init__(self):
        # Dinamikus viselkedéshez szükséges változók definíciója
        self.oldpos = None
        self.oldcounter = 0

    # Egyéb függvények...
    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    # Az egyetlen kötelező elem: A játékmestertől jövő információt feldolgozó és választ elküldő függvény
    def processObservation(self, fulljson, sendData):
        """
        :param fulljson: A játékmestertől érkező JSON dict-be konvertálva.
        Két kötelező kulccsal: 'type' (leaderBoard, readyToStart, started, gameData, serverClose) és 'payload' (az üzenet adatrésze).
        'leaderBoard' type a játék végét jelzi, a payload tartalma {'ticks': a játék hossza tickekben, 'players':[{'name': jáétékosnév, 'active': él-e a játékos?, 'maxSize': a legnagyobb elért méret a játék során},...]}
        'readyToStart' type esetén a szerver az indító üzenetre vár esetén, a payload üres (None)
        'started' type esetén a játék elindul, tickLength-enként kiküldés és akciófogadás várható payload {'tickLength': egy tick hossza }
        'gameData' type esetén az üzenet a játékos által elérhető információkat küldi, a payload:
                                    {"pos": abszolút pozíció a térképen, "tick": az aktuális tick sorszáma, "active": a saját életünk állapota,
                                    "size": saját méret,
                                    "leaderBoard": {'ticks': a játék hossza tickekben eddig, 'players':[{'name': jáétékosnév, 'active': él-e a játékos?, 'maxSize': a legnagyobb elért méret a játék során eddig},...]},
                                    "vision": [{"relative_coord": az adott megfigyelt mező relatív koordinátája,
                                                                    "value": az adott megfigyelt mező értéke (0-3,9),
                                                                    "player": None, ha nincs aktív játékos, vagy
                                                                            {name: a mezőn álló játékos neve, size: a mezőn álló játékos mérete}},...] }
        'serverClose' type esetén a játékmester szabályos, vagy hiba okozta bezáródásáról értesülünk, a payload üres (None)
        :param sendData: A kliens adatküldő függvénye, JSON formátumú str bemenetet vár, melyet a játékmester felé továbbít.
        Az elküldött adat struktúrája {"command": Parancs típusa, "name": A küldő azonosítója, "payload": az üzenet adatrésze}
        Elérhető parancsok:
        'SetName' A kliens felregisztrálja a saját nevét a szervernek, enélkül a nevünkhöz tartozó üzenetek nem térnek vissza.
                 Tiltott nevek: a configban megadott játékmester név és az 'all'.
        'SetAction' Ebben az esetben a payload az akció string, amely két karaktert tartalmaz az X és az Y koordináták (matematikai mátrix indexelés) menti elmozdulásra.
                a karakterek értékei '0': helybenmaradás az adott tengely mentén, '+' pozitív irányú lépés, '-' negatív irányú lépés lehet. Amennyiben egy tick ideje alatt
                nem külünk értéket az alapértelmezett '00' kerül végrehajtásra.
        'GameControl' üzeneteket csak a Config.py-ban megadott játékmester névvel lehet küldeni, ezek a játékmenetet befolyásoló üzenetek.
                A payload az üzenet típusát (type), valamint az ahhoz tartozó 'data' adatokat kell, hogy tartalmazza.
                    'start' type elindítja a játékot egy "readyToStart" üzenetet küldött játék esetén, 'data' mezője üres (None)
                    'reset' type egy játék után várakozó 'leaderBoard'-ot küldött játékot állít alaphelyzetbe. A 'data' mező
                            {'mapPath':None, vagy elérési útvonal, 'updateMapPath': None, vagy elérési útvonal} formátumú, ahol None
                            esetén az előző pálya és növekedési map kerül megtartásra, míg elérési útvonal megadása esetén új pálya kerül betöltésre annak megfelelően.
                    'interrupt' type esetén a 'data' mező üres (None), ez megszakítja a szerver futását és szabályosan leállítja azt.
        :return:
        """
        # Játék rendezéssel kapcsolatos üzenetek lekezelése
        if fulljson["type"] == "leaderBoard":
            print("Game finished after",fulljson["payload"]["ticks"],"ticks!")
            print("Leaderboard:")
            for score in fulljson["payload"]["players"]:
                print(score["name"],score["active"], score["maxSize"])

            time.sleep(50)
            sendData(json.dumps({"command": "GameControl", "name": "master",
                                 "payload": {"type": "reset", "data": {"mapPath": None, "updateMapPath": None}}}))

        if fulljson["type"] == "readyToStart":
            print("Game is ready, starting in 5")
            time.sleep(5)
            sendData(json.dumps({"command": "GameControl", "name": "master",
                                 "payload": {"type": "start", "data": None}}))

        if fulljson["type"] == "started":
            print("Startup message from server.")
            print("Ticks interval is:",fulljson["payload"]["tickLength"])


        # Akció előállítása bemenetek alapján (egyezik a NaiveHunterBot-okéval)
        elif fulljson["type"] == "gameData":
            jsonData = fulljson["payload"]
            if "pos" in jsonData.keys() and "tick" in jsonData.keys() and "active" in jsonData.keys() and "size" in jsonData.keys() and "vision" in jsonData.keys():
                if self.oldpos is not None:
                    oldoldpos = np.loadtxt('oldoldpos1.txt')
                    if tuple(self.oldpos) == tuple(jsonData["pos"]):
                        self.oldcounter += 1
                    #else:
                        #self.oldcounter = 0
                    elif tuple(oldoldpos) == tuple(jsonData["pos"]):
                        self.oldcounter += 1
                    np.savetxt('oldoldpos1.txt', np.asarray(self.oldpos))

                if jsonData["active"]:
                    self.oldpos = jsonData["pos"].copy()

                vals = []
                for field in jsonData["vision"]:
                    if field["player"] is not None:
                        if tuple(field["relative_coord"]) == (0, 0):
                            if 0 < field["value"] <= 3:
                                vals.append(field["value"])
                            elif field["value"] == 9:
                                vals.append(field["value"])
                            else:
                                vals.append(0)
                        elif field["player"]["size"] * 1.15 < jsonData["size"]:
                            vals.append(field["player"]["size"])
                        elif field["player"]["size"] * 1.05 > jsonData["size"]:
                            vals.append(-1)
                        else:
                            vals.append(0)
                    else:
                        if 0 < field["value"] <= 3:
                            vals.append(field["value"])
                        elif field["value"] == 9:
                            vals.append(field["value"])
                        else:
                            vals.append(0)

                values = np.array(vals)
                if np.max(values) <= 0 or self.oldcounter >= 1:
                    actstring = self.getRandomAction()
                    self.oldcounter = 0
                else:
                    xfal=0
                    yfal=0
                    xkaja=0
                    ykaja=0
                    xkoord=0
                    ykoord=0
                    xenemy=0
                    yenemy=0

                    szorzo = 1;

                    for i in range(81):
                        if i == 29 or i == 30 or i == 31 or i == 39 or i == 41 or i == 49 or i == 50 or i == 51:
                            szorzo = 1 / 5.811158847063779831e-01;

                        if values[i] == 9:
                            if koord[i][0] != 0:
                                if koord[i][1] == 0:
                                    masik = 3
                                else:
                                    masik = abs(1 / koord[i][1])
                                if 0 > koord[i][0]:
                                    xfal += szorzo * masik * abs(1 / koord[i][0]) ** (1/5.041653884109109640e-01)
                                else:
                                    xfal -= szorzo * masik * abs(1 / koord[i][0]) ** (1/5.041653884109109640e-01)
                            if koord[i][1] != 0:
                                if koord[i][0] == 0:
                                    masik = 3
                                else:
                                    masik = abs(1 / koord[i][0])
                                if 0 > koord[i][0]:
                                    yfal += szorzo * masik * abs(1 / koord[i][1]) ** (1/5.041653884109109640e-01)
                                else:
                                    yfal -= szorzo * masik * abs(1 / koord[i][1]) ** (1/5.041653884109109640e-01)

                        elif values[i] > 0:
                            if koord[i][0] != 0:
                                if koord[i][1] == 0:
                                    masik = 3
                                else:
                                    masik = abs(1 / koord[i][1])
                                if 0 > koord[i][0]:
                                    xkaja -= szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/9.817419855389744043e-01)
                                else:
                                    xkaja += szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/9.817419855389744043e-01)

                            if koord[i][1] != 0:
                                if koord[i][0] == 0:
                                    masik = 3
                                else:
                                    masik = abs(1 / koord[i][0])
                                if 0 > koord[i][1]:
                                    ykaja -= szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/9.817419855389744043e-01)
                                else:
                                    ykaja += szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/9.817419855389744043e-01)


                        elif 0 > values[i]:
                            if koord[i][0] != 0:
                                if koord[i][1] == 0:
                                    masik = 3
                                else:
                                    masik = abs(1 / koord[i][1])
                                if 0 > koord[i][0]:
                                    xenemy += szorzo * masik * abs(1 / koord[i][0]) ** (1/6.774830534122884274e-01)
                                else:
                                    xenemy -= szorzo * masik * abs(1 / koord[i][0]) ** (1/6.774830534122884274e-01)
                            if koord[i][1] != 0:
                                if koord[i][0] == 0:
                                    masik = 3
                                else:
                                    masik = abs(1 / koord[i][0])
                                if 0 > koord[i][0]:
                                    yenemy += szorzo * masik * abs(1 / koord[i][1]) ** (1/6.774830534122884274e-01)
                                else:
                                    yenemy -= szorzo * masik * abs(1 / koord[i][1]) ** (1/6.774830534122884274e-01)

                    xkozep = (19.5-jsonData["pos"][0])/2*(1 / 8.234386530239135027e-01)
                    ykozep = (19.5-jsonData["pos"][1])/2*(1 / 8.234386530239135027e-01)
                    xkoord = xfal+xkaja*9.323730617761611938e-01+xenemy*6.852176893502473831e-01+xkozep
                    ykoord = yfal+ykaja*9.323730617761611938e-01+yenemy*6.852176893502473831e-01+ykozep

                    actdict = {0: "0", 1: "+", 2: "-"}
                    action=""

                    if abs(xkoord) > (1 / 5.346625798847526312e-01) * abs(ykoord):
                        if xkoord > 0:
                            r = np.array([1, 0])
                            for act in r:
                                action += actdict[act]
                        else:
                            r = np.array([2, 0])
                            for act in r:
                                action += actdict[act]

                    elif abs(ykoord) > (1 / 5.346625798847526312e-01) * abs(xkoord):
                        if ykoord > 0:
                            r = np.array([0, 1])
                            for act in r:
                                action += actdict[act]
                        else:
                            r = np.array([0, 2])
                            for act in r:
                                action += actdict[act]
                    elif xkoord > 0:
                        if ykoord > 0:
                            r = np.array([1, 1])
                            for act in r:
                                action += actdict[act]
                        else:
                            r = np.array([1, 2])
                            for act in r:
                                action += actdict[act]

                    else:
                        if ykoord > 0:
                            r = np.array([2, 1])
                            for act in r:
                                action += actdict[act]
                        else:
                            r = np.array([2, 2])
                            for act in r:
                                action += actdict[act]

                    actstring = action

                if actstring == '0-' and values[39]==9:
                    actstring = '+-'
                if actstring == '+-' and values[49]==9:
                    actstring = '+0'
                if actstring == '+0' and values[50]==9:
                    actstring = '++'
                if actstring == '++' and values[51]==9:
                    actstring = '0+'
                if actstring == '0+' and values[41]==9:
                    actstring = '-+'
                if actstring == '-+' and values[31]==9:
                    actstring = '-0'
                if actstring == '-0' and values[30]==9:
                    actstring = '--'
                if actstring == '--' and values[29]==9:
                    actstring = '0-'

                if actstring == '0-' and values[39]==9:
                    actstring = '+-'
                if actstring == '+-' and values[49]==9:
                    actstring = '+0'
                if actstring == '+0' and values[50]==9:
                    actstring = '++'
                if actstring == '++' and values[51]==9:
                    actstring = '0+'
                if actstring == '0+' and values[41]==9:
                    actstring = '-+'
                if actstring == '-+' and values[31]==9:
                    actstring = '-0'
                if actstring == '-0' and values[30]==9:
                    actstring = '--'
                if actstring == '--' and values[29]==9:
                    actstring = '0-'


                # Akció JSON előállítása és elküldése
                sendData(json.dumps({"command": "SetAction", "name": "Pink", "payload": actstring}))



if __name__=="__main__":
    # Példányosított stratégia objektum
    hunter = RemoteNaiveHunterStrategy()

    # Socket kliens, melynek a szerver címét kell megadni (IP, port), illetve a callback függvényt, melynek szignatúrája a fenti
    # callback(fulljson, sendData)
    client = SocketClient("10.0.0.113", 42069, hunter.processObservation)

    # Kliens indítása
    client.start()
    # Kis szünet, hogy a kapcsolat felépülhessen, a start nem blockol, a kliens külső szálon fut
    time.sleep(0.1)
    # Regisztráció a megfelelő névvel
    client.sendData(json.dumps({"command": "SetName", "name": "Pink", "payload": None}))

    # Nincs blokkoló hívás, a főszál várakozó állapotba kerül, itt végrehajthatók egyéb műveletek a kliens automata működésétől függetlenül.
