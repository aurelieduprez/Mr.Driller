#! MAIN POUR LE MENU
from os import path



def refreshScore(newScore):


    contenu = open(path.join("Assets","Score","score.txt"), "r").read()    #! read permet de traiter le fichier ligne par ligne , retour une liste contenant les lignes
    print(contenu)
    score = str(contenu)   #! exemple
    score = score.split("#")   #! à chaque "#" séparer en plusieurs éléments j
    for i in range (len(score)):
        score[i] = int(score[i])    #! caste la variable score en entiers    (comme ça on peut faire un append
    print (score)
    score.append(newScore)        #! ajouter le dernier score a la liste

    with open(path.join("Assets","Score","score.txt"), "w") as fichier:
        score.sort(reverse=True)    #! True -> ordre décroissant
        print(score)
        for i in range(len(score)):
            score[i] = str(score[i])    #! cast en string pour pouvoir join
        line = "#".join(score)    #! join = coller tous les éléments de la liste, avec des "#" entre les éléments
        print(line)
        fichier.write(line)









