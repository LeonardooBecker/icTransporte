import os

def listaPastas(diretorio):
    pastas = os.listdir(diretorio)

    elementos=[]
    for elem in pastas:
        if not os.path.isfile(elem):
            if not "pycache" in elem:
                elementos.append(elem)

    return elementos