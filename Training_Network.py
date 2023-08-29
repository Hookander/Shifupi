"""Va prendre les images de la caméra, ie les distances entre les doigts,
    pour apprednre à reconnaitre les gestes du shifumi
"""

import network
rockfile = open(files/ro)
#nombre de distances utlisées
nb_dist = 4

net = network.Network([4, 5, 3])

'''
Mtn on extrait les distances des fichiers txt
'''