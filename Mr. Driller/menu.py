#! MAIN POUR LE MENU
from os import path


def refreshScore(newScore):

    content = open(path.join("Assets", "Score", "score.txt"), "r").read()    # Read file line by line
    print(content)
    score = str(content)
    score = score.split("#")   # Splits by "#"
    for i in range(len(score)):
        score[i] = int(score[i])
    score.append(newScore)  # adds score to list

    with open(path.join("Assets", "Score", "score.txt"), "w") as scoreFile:
        score.sort(reverse=True)    # sorts from biggest to smallest
        for i in range(len(score)):
            score[i] = str(score[i])
        line = "#".join(score)
        scoreFile.write(line)

    scoreFile.close()









