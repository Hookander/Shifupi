"""Va prendre les images de la caméra, ie les distances entre les doigts,
    pour apprednre à reconnaitre les gestes du shifumi
"""

import network

rockfile = open('files/rockDistances.txt', 'r')
paperfile = open('files/paperDistances.txt', 'r')
scissorsfile = open('files/scissorsDistances.txt', 'r')


#nombre de distances utlisées
nb_dist = 4

net = network.Network([4, 5, 3])

'''
Mtn on extrait les distances des fichiers txt
Pour chaque geste, on doit finalement obtenir un tableau contenant des tuples de la forme
([[], [], []], [[]]) (des vecteurs) avec en 1 les distances et en 2 le signe

[1, 0, 0] -> ROCK
[0, 1, 0] -> PAPER
[0, 0, 1] -> SCISSORS
'''
class Gesture(object):
    pass
class Rock(Gesture):
    def __init__(self):
        self.tab = [1, 0, 0]
class Paper(Gesture):
    def __init__(self):
        self.tab = [0, 1, 0]
class Scissors(Gesture):
    def __init__(self):
        self.tab = [0, 0, 1]
    

def extract_data(gesture):
    match gesture:
        case Rock():
            print("rock")
            file = rockfile
        case Paper():
            file = paperfile
        case Scissors():
            file = scissorsfile
    lines = file.readlines()
    '''
        Pour l'exemple si on travaille avec 4 distances, alors les nombres en position 0, 5, 10, etc..
        représentent la numéro de l'image, et donc ne nous intéressent pas, on peut donc les sauter
        et puis il faut ensuite répartir les données restantes
    '''
    lines1 = []
    for i in range(len(lines)):
        if i%5 != 0:
            lines1.append(lines[i].split())

    return lines1[0:10]
print(extract_data(Rock()))
    

