import numpy as np
import json
from LearningAlgorithm import *
import random

koord = [[-5, 0], [-4, -3], [-4, -2], [-4, -1], [-4, 0], [-4, 1], [-4, 2], [-4, 3], [-3, -4], [-3, -3], [-3, -2], [-3, -1], [-3, 0], [-3, 1], [-3, 2], [-3, 3], [-3, 4], [-2, -4], [-2, -3], [-2, -2], [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3], [-2, 4], [-1, -4], [-1, -3], [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3], [-1, 4], [0, -5], [0, -4], [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, -4], [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, -4], [2, -3], [2, -2], [2, -1], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, -4], [3, -3], [3, -2], [3, -1], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, -3], [4, -2], [4, -1], [4, 0], [4, 1], [4, 2], [4, 3], [5, 0]]


#activation1 = Activation_ReLU()
#activation2 = Activation_Softmax()

class RemotePlayerStrategy:


    def __init__(self, **kwargs):
        self.nextAction = "0"
        self.oldpos = None
        self.oldcounter = 0

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def setObservations(self, ownObject, fieldDict):
        self.nextAction = "0"
        self.sendData(json.dumps({"type":"gameData", "payload":fieldDict}), ownObject.name)


    def getNextAction(self):
        return self.nextAction

    def reset(self):
        self.nextAction = "0"


class DummyStrategy:


    def __init__(self, **kwargs):
        self.nextAction = "0"
        self.oldpos = None
        self.oldcounter = 0

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def setObservations(self, ownObject, fieldDict):
        if self.oldpos is not None:
            oldoldpos = np.loadtxt('oldoldpos3.txt')
            if tuple(self.oldpos) == tuple(ownObject.pos):
                self.oldcounter += 1

            elif tuple(oldoldpos) == tuple(ownObject.pos):
                self.oldcounter += 1
                #print('ugrál')

            #print(str(oldoldpos) + ' - ' + str(ownObject.pos))
            np.savetxt('oldoldpos3.txt', np.asarray(self.oldpos))
        #print(np.asarray(self.oldpos))
        #np.savetxt('oldoldpos.txt', np.asarray(self.oldpos))

        self.oldpos = ownObject.pos.copy()



        values = []

        for field in fieldDict["vision"]:
            if field["player"] is not None:
                if tuple(field["relative_coord"]) == (0, 0):
                    if 0 < field["value"] <= 3:
                        values.append(field["value"])
                    elif field["value"] == 9:
                        values.append(field["value"])
                    else:
                        values.append(0)
                elif field["player"]["size"] * 1.1 < ownObject.size:
                    values.append(field["player"]["size"])
                elif field["player"]["size"] * 1.1 > ownObject.size:
                    values.append(-1)
                else:
                    values.append(0)
            else:
                if 0 < field["value"] <= 3:
                    values.append(field["value"])
                elif field["value"] == 9:
                    values.append(field["value"])
                else:
                    values.append(0)


        if np.max(values) == 0 or self.oldcounter >= 1:
            self.nextAction = self.getRandomAction()
            #print(self.nextAction)
            #print('Random lépek')
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
                    szorzo = 1 / 4.117069707717746496e-01;

                if values[i] == 9:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xfal += szorzo * masik * abs(1 / koord[i][0]) ** (1/5.009192219004034996e-01)
                        else:
                            xfal -= szorzo * masik * abs(1 / koord[i][0]) ** (1/5.009192219004034996e-01)
                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][0]:
                            yfal += szorzo * masik * abs(1 / koord[i][1]) ** (1/5.009192219004034996e-01)
                        else:
                            yfal -= szorzo * masik * abs(1 / koord[i][1]) ** (1/5.009192219004034996e-01)

                elif values[i] > 0:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xkaja -= szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/7.137815093155950308e-01)
                        else:
                            xkaja += szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/7.137815093155950308e-01)

                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][1]:
                            ykaja -= szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/7.137815093155950308e-01)
                        else:
                            ykaja += szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/7.137815093155950308e-01)


                elif 0 > values[i]:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xenemy += szorzo * masik * abs(1 / koord[i][0]) ** (1/7.411406070459634066e-01)
                        else:
                            xenemy -= szorzo * masik * abs(1 / koord[i][0]) ** (1/7.411406070459634066e-01)
                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][0]:
                            yenemy += szorzo * masik * abs(1 / koord[i][1]) ** (1/7.411406070459634066e-01)
                        else:
                            yenemy -= szorzo * masik * abs(1 / koord[i][1]) ** (1/7.411406070459634066e-01)

            xkozep = (19.5-ownObject.pos[0])*(1 / 4.079428613185882568e-01)
            ykozep = (19.5-ownObject.pos[1])*(1 / 4.079428613185882568e-01)
            xkoord = xfal+xkaja*7.386791510507464409e-01+xenemy*7.057257865089923143e-01+xkozep
            ykoord = yfal+ykaja*7.386791510507464409e-01+yenemy*7.057257865089923143e-01+ykozep

            actdict = {0: "0", 1: "+", 2: "-"}
            action=""

            if abs(xkoord) > (1 / 3.707341423723846674e-01) * abs(ykoord):
                if xkoord > 0:
                    r = np.array([1, 0])
                    for act in r:
                        action += actdict[act]
                else:
                    r = np.array([2, 0])
                    for act in r:
                        action += actdict[act]

            elif abs(ykoord) > (1 / 3.707341423723846674e-01) * abs(xkoord):
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

            self.nextAction = action

        if self.nextAction == '0-' and values[39]==9:
            self.nextAction = '+-'
        if self.nextAction == '+-' and values[49]==9:
            self.nextAction = '+0'
        if self.nextAction == '+0' and values[50]==9:
            self.nextAction = '++'
        if self.nextAction == '++' and values[51]==9:
            self.nextAction = '0+'
        if self.nextAction == '0+' and values[41]==9:
            self.nextAction = '-+'
        if self.nextAction == '-+' and values[31]==9:
            self.nextAction = '-0'
        if self.nextAction == '-0' and values[30]==9:
            self.nextAction = '--'
        if self.nextAction == '--' and values[29]==9:
            self.nextAction = '0-'

        if self.nextAction == '0-' and values[39]==9:
            self.nextAction = '+-'
        if self.nextAction == '+-' and values[49]==9:
            self.nextAction = '+0'
        if self.nextAction == '+0' and values[50]==9:
            self.nextAction = '++'
        if self.nextAction == '++' and values[51]==9:
            self.nextAction = '0+'
        if self.nextAction == '0+' and values[41]==9:
            self.nextAction = '-+'
        if self.nextAction == '-+' and values[31]==9:
            self.nextAction = '-0'
        if self.nextAction == '-0' and values[30]==9:
            self.nextAction = '--'
        if self.nextAction == '--' and values[29]==9:
            self.nextAction = '0-'




    def getNextAction(self):
        return self.nextAction

    def reset(self):
        self.nextAction = "0"


class RandBotStrategy:


    def __init__(self, **kwargs):
        self.nextAction = "0"
        self.oldpos = None
        self.oldcounter = 0

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def setObservations(self, ownObject, fieldDict):
        if self.oldpos is not None:
            oldoldpos = np.loadtxt('oldoldpos.txt')
            if tuple(self.oldpos) == tuple(ownObject.pos):
                self.oldcounter += 1

            elif tuple(oldoldpos) == tuple(ownObject.pos):
                self.oldcounter += 1
                #print('ugrál')

            np.savetxt('oldoldpos.txt', np.asarray(self.oldpos))
        self.oldpos = ownObject.pos.copy()


        values = []

        for field in fieldDict["vision"]:
            if field["player"] is not None:
                if tuple(field["relative_coord"]) == (0, 0):
                    if 0 < field["value"] <= 3:
                        values.append(field["value"])
                    elif field["value"] == 9:
                        values.append(field["value"])
                    else:
                        values.append(0)
                elif field["player"]["size"] * 1.15 < ownObject.size:
                    values.append(field["player"]["size"])
                elif field["player"]["size"] * 1.05 > ownObject.size:
                    values.append(-1)
                else:
                    values.append(0)
            else:
                if 0 < field["value"] <= 3:
                    values.append(field["value"])
                elif field["value"] == 9:
                    values.append(field["value"])
                else:
                    values.append(0)


        if np.max(values) == 0 or self.oldcounter >= 2:
            self.nextAction = self.getRandomAction()
            #print(self.nextAction)
            #print('Random lépek')
            self.oldcounter = 0

        else:
            weights = np.loadtxt("weights_act.txt")

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
                    szorzo = 1 / weights[6];

                if values[i] == 9:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xfal += szorzo * masik * abs(1 / koord[i][0]) ** (1/weights[0])
                        else:
                            xfal -= szorzo * masik * abs(1 / koord[i][0]) ** (1/weights[0])
                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][0]:
                            yfal += szorzo * masik * abs(1 / koord[i][1]) ** (1/weights[0])
                        else:
                            yfal -= szorzo * masik * abs(1 / koord[i][1]) ** (1/weights[0])

                elif values[i] > 0:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xkaja -= szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/weights[1])
                        else:
                            xkaja += szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/weights[1])

                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][1]:
                            ykaja -= szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/weights[1])
                        else:
                            ykaja += szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/weights[1])


                elif 0 > values[i]:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xenemy += szorzo * masik * abs(1 / koord[i][0]) ** (1/weights[4])
                        else:
                            xenemy -= szorzo * masik * abs(1 / koord[i][0]) ** (1/weights[4])
                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][0]:
                            yenemy += szorzo * masik * abs(1 / koord[i][1]) ** (1/weights[4])
                        else:
                            yenemy -= szorzo * masik * abs(1 / koord[i][1]) ** (1/weights[4])

            xkozep = (19.5-ownObject.pos[0])*(1 / weights[7])
            ykozep = (19.5-ownObject.pos[1])*(1 / weights[7])
            xkoord = xfal+xkaja*weights[2]+xenemy*weights[5]+xkozep
            ykoord = yfal+ykaja*weights[2]+yenemy*weights[5]+ykozep

            actdict = {0: "0", 1: "+", 2: "-"}
            action=""

            if abs(xkoord) > (1 / weights[3]) * abs(ykoord):
                if xkoord > 0:
                    r = np.array([1, 0])
                    for act in r:
                        action += actdict[act]
                else:
                    r = np.array([2, 0])
                    for act in r:
                        action += actdict[act]

            elif abs(ykoord) > (1 / weights[3]) * abs(xkoord):
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

            self.nextAction = action

        if self.nextAction == '0-' and values[39]==9:
            self.nextAction = '+-'
        if self.nextAction == '+-' and values[49]==9:
            self.nextAction = '+0'
        if self.nextAction == '+0' and values[50]==9:
            self.nextAction = '++'
        if self.nextAction == '++' and values[51]==9:
            self.nextAction = '0+'
        if self.nextAction == '0+' and values[41]==9:
            self.nextAction = '-+'
        if self.nextAction == '-+' and values[31]==9:
            self.nextAction = '-0'
        if self.nextAction == '-0' and values[30]==9:
            self.nextAction = '--'
        if self.nextAction == '--' and values[29]==9:
            self.nextAction = '0-'

        if self.nextAction == '0-' and values[39]==9:
            self.nextAction = '+-'
        if self.nextAction == '+-' and values[49]==9:
            self.nextAction = '+0'
        if self.nextAction == '+0' and values[50]==9:
            self.nextAction = '++'
        if self.nextAction == '++' and values[51]==9:
            self.nextAction = '0+'
        if self.nextAction == '0+' and values[41]==9:
            self.nextAction = '-+'
        if self.nextAction == '-+' and values[31]==9:
            self.nextAction = '-0'
        if self.nextAction == '-0' and values[30]==9:
            self.nextAction = '--'
        if self.nextAction == '--' and values[29]==9:
            self.nextAction = '0-'


    def getNextAction(self):
        return self.nextAction

    def reset(self):
        self.nextAction = "0"





class NaiveStrategy:

    def __init__(self, **kwargs):
        self.nextAction = "0"
        self.oldpos = None
        self.oldcounter = 0

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def setObservations(self, ownObject, fieldDict):
        if self.oldpos is not None:
            oldoldpos = np.loadtxt('oldoldpos4.txt')
            if tuple(self.oldpos) == tuple(ownObject.pos):
                self.oldcounter += 1

            elif tuple(oldoldpos) == tuple(ownObject.pos):
                self.oldcounter += 1
            np.savetxt('oldoldpos4.txt', np.asarray(self.oldpos))

        self.oldpos = ownObject.pos.copy()


        values = []

        for field in fieldDict["vision"]:
            if field["player"] is not None:
                if tuple(field["relative_coord"]) == (0, 0):
                    if 0 < field["value"] <= 3:
                        values.append(field["value"])
                    elif field["value"] == 9:
                        values.append(field["value"])
                    else:
                        values.append(0)
                elif field["player"]["size"] * 1.1 < ownObject.size:
                    values.append(field["player"]["size"])
                elif field["player"]["size"] * 1.1 > ownObject.size:
                    values.append(-1)
                else:
                    values.append(0)
            else:
                if 0 < field["value"] <= 3:
                    values.append(field["value"])
                elif field["value"] == 9:
                    values.append(field["value"])
                else:
                    values.append(0)


        if np.max(values) == 0 or self.oldcounter >= 1:
            self.nextAction = self.getRandomAction()
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
                    szorzo = 1 / 4.117069707717746496e-01;

                if values[i] == 9:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xfal += szorzo * masik * abs(1 / koord[i][0]) ** (1/5.009192219004034996e-01)
                        else:
                            xfal -= szorzo * masik * abs(1 / koord[i][0]) ** (1/5.009192219004034996e-01)
                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][0]:
                            yfal += szorzo * masik * abs(1 / koord[i][1]) ** (1/5.009192219004034996e-01)
                        else:
                            yfal -= szorzo * masik * abs(1 / koord[i][1]) ** (1/5.009192219004034996e-01)

                elif values[i] > 0:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xkaja -= szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/7.137815093155950308e-01)
                        else:
                            xkaja += szorzo * values[i] * masik * abs(1 / koord[i][0]) ** (1/7.137815093155950308e-01)

                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][1]:
                            ykaja -= szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/7.137815093155950308e-01)
                        else:
                            ykaja += szorzo * values[i] * masik * abs(1 / koord[i][1]) ** (1/7.137815093155950308e-01)


                elif 0 > values[i]:
                    if koord[i][0] != 0:
                        if koord[i][1] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][1])
                        if 0 > koord[i][0]:
                            xenemy += szorzo * masik * abs(1 / koord[i][0]) ** (1/7.411406070459634066e-01)
                        else:
                            xenemy -= szorzo * masik * abs(1 / koord[i][0]) ** (1/7.411406070459634066e-01)
                    if koord[i][1] != 0:
                        if koord[i][0] == 0:
                            masik = 3
                        else:
                            masik = abs(1 / koord[i][0])
                        if 0 > koord[i][0]:
                            yenemy += szorzo * masik * abs(1 / koord[i][1]) ** (1/7.411406070459634066e-01)
                        else:
                            yenemy -= szorzo * masik * abs(1 / koord[i][1]) ** (1/7.411406070459634066e-01)

            xkozep = (19.5-ownObject.pos[0])*(1 / 4.079428613185882568e-01)
            ykozep = (19.5-ownObject.pos[1])*(1 / 4.079428613185882568e-01)
            xkoord = xfal+xkaja*7.386791510507464409e-01+xenemy*7.057257865089923143e-01+xkozep
            ykoord = yfal+ykaja*7.386791510507464409e-01+yenemy*7.057257865089923143e-01+ykozep

            actdict = {0: "0", 1: "+", 2: "-"}
            action=""

            if abs(xkoord) > (1 / 3.707341423723846674e-01) * abs(ykoord):
                if xkoord > 0:
                    r = np.array([1, 0])
                    for act in r:
                        action += actdict[act]
                else:
                    r = np.array([2, 0])
                    for act in r:
                        action += actdict[act]

            elif abs(ykoord) > (1 / 3.707341423723846674e-01) * abs(xkoord):
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

            self.nextAction = action

        if self.nextAction == '0-' and values[39]==9:
            self.nextAction = '+-'
        if self.nextAction == '+-' and values[49]==9:
            self.nextAction = '+0'
        if self.nextAction == '+0' and values[50]==9:
            self.nextAction = '++'
        if self.nextAction == '++' and values[51]==9:
            self.nextAction = '0+'
        if self.nextAction == '0+' and values[41]==9:
            self.nextAction = '-+'
        if self.nextAction == '-+' and values[31]==9:
            self.nextAction = '-0'
        if self.nextAction == '-0' and values[30]==9:
            self.nextAction = '--'
        if self.nextAction == '--' and values[29]==9:
            self.nextAction = '0-'

        if self.nextAction == '0-' and values[39]==9:
            self.nextAction = '+-'
        if self.nextAction == '+-' and values[49]==9:
            self.nextAction = '+0'
        if self.nextAction == '+0' and values[50]==9:
            self.nextAction = '++'
        if self.nextAction == '++' and values[51]==9:
            self.nextAction = '0+'
        if self.nextAction == '0+' and values[41]==9:
            self.nextAction = '-+'
        if self.nextAction == '-+' and values[31]==9:
            self.nextAction = '-0'
        if self.nextAction == '-0' and values[30]==9:
            self.nextAction = '--'
        if self.nextAction == '--' and values[29]==9:
            self.nextAction = '0-'

    def getNextAction(self):
        return self.nextAction

    def reset(self):
        self.nextAction = "0"


class NaiveHunterStrategy:
    def __init__(self, **kwargs):
        self.nextAction = "0"
        self.oldpos = None
        self.oldcounter = 0

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def setObservations(self, ownObject, fieldDict):
        if self.oldpos is not None:
            if tuple(self.oldpos) == tuple(ownObject.pos):
                self.oldcounter += 1
            else:
                self.oldcounter = 0
        if ownObject.active:
            self.oldpos = ownObject.pos.copy()

        vals = []
        for field in fieldDict["vision"]:
            if field["player"] is not None:
                if tuple(field["relative_coord"]) == (0, 0):
                    if 0 < field["value"] <= 3:
                        vals.append(field["value"])
                    elif field["value"] == 9:
                        vals.append(-1)
                    else:
                        vals.append(0)
                elif field["player"]["size"] * 1.1 < ownObject.size:
                    vals.append(field["player"]["size"])
                else:
                    vals.append(-1)
            else:
                if 0 < field["value"] <= 3:
                    vals.append(field["value"])
                elif field["value"] == 9:
                    vals.append(-1)
                else:
                    vals.append(0)

        values = np.array(vals)
        if np.max(values) <= 0 or self.oldcounter >= 3:
            self.nextAction = self.getRandomAction()
            self.oldcounter = 0
        else:
            idx = np.argmax(values)
            actstring = ""
            for i in range(2):
                if fieldDict["vision"][idx]["relative_coord"][i] == 0:
                    actstring += "0"
                elif fieldDict["vision"][idx]["relative_coord"][i] > 0:
                    actstring += "+"
                elif fieldDict["vision"][idx]["relative_coord"][i] < 0:
                    actstring += "-"

            self.nextAction = actstring

    def getNextAction(self):
        return self.nextAction

    def reset(self):
        self.nextAction = "0"

class LearningPlayerStrategy:
    def __init__(self, **kwargs):
        self.nextAction = 0

    def setObservations(self, ownObject, fieldDict):
        values = np.array([field["value"] for field in fieldDict["vision"]])
        file2 = open('field.txt', 'w')
        file2.write(str(values))
        file2.close()
        pass

    def getNextAction(self):
        action = getActionFromOutside()
        return action

    def reset(self):
        self.nextAction = "0"


class Player:
    strategies = {"randombot": RandBotStrategy, "naivebot": NaiveStrategy, "naivehunterbot": NaiveHunterStrategy,
                  "remoteplayer": RemotePlayerStrategy, "dummy":DummyStrategy, "learningplayer": LearningPlayerStrategy}

    def __init__(self, name, playerType, startingSize, **kwargs):
        self.name = name
        self.playerType = playerType
        self.pos = np.zeros((2,))
        self.size = startingSize
        kwargs["name"] = name
        self.strategy = Player.strategies[playerType](**kwargs)
        self.active = True

    def die(self):
        self.active = False
        print(self.name + " died!")

    def reset(self):
        self.active = True
