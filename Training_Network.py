"""Va prendre les images de la caméra, ie les distances entre les doigts,
    pour apprednre à reconnaitre les gestes du shifumi
"""
#! parfois il y a des problèmes dans les txt ou un numéro n'est pas noté -> décale tout et le programme plante
#! peut être une bonne idée de carrément enlever ces numéros qui servent pas à grand chose finalement

import network
import numpy as np
import time

rockfile = open('files/rockDistances.txt', 'r')
paperfile = open('files/paperDistances.txt', 'r')
scissorsfile = open('files/scissorsDistances.txt', 'r')


#nombre de distances utlisées
nb_dist = 4

net = network.Network([4, 50, 10, 3])

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
        self.vect = [[1], [0], [0]]
class Paper(Gesture):
    def __init__(self):
        self.tab = [0, 1, 0]
        self.vect = [[0], [1], [0]]
class Scissors(Gesture):
    def __init__(self):
        self.tab = [0, 0, 1]
        self.vect = [[0], [0], [1]]
    

def extract_data(gesture):
    match gesture:
        case Rock():
            file = rockfile
        case Paper():
            file = paperfile
        case Scissors():
            file = scissorsfile
    output = gesture.vect
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
    
    '''
    lines1 ici de la forme [['8', '167.50520561209547'],..]
    '''
    trainingData = []
    for i in range(0, len(lines1), nb_dist):
        input = []
        for j in range(nb_dist):
            input.append([float(lines1[i+j][1])/200])
        trainingData.append((np.array(input), np.array(output)))
    
    return trainingData

trainingData = extract_data(Scissors()) + extract_data(Rock()) + extract_data(Paper())
np.random.shuffle(trainingData)
testData = trainingData
net.SGD(trainingData, 5, 1, 1, testData)
#On sauvegarde alors les coeffs du réseau dans un fichier texte

#test = np.array([[157.0516653030859/200],[93.15978391386966/200],[38.10050882851033/200],[47.23414238541866/200]])
#test = np.array([[445.67722465359077/200], [486.86747122360936/200], [451.94716415162605/200], [367.88451568147497/200]])
test = np.array([[285.01326278739262/200], [278.68163087570906/200], [16.77027263074721/200], [32.93207452061093/200]])

result = net.feedforward(test).transpose()[0]
result = net.smooth_result(result)
print(result)
named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m-%d-%Y %Hh %Mm %Ss", named_tuple)
save_file = open("Network Data/"+time_string+'.txt', "w")
save_file.write(str(net.biases) + "\n")
save_file.write(str(net.weights))
save_file.close()