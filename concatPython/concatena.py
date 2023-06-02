import os
import subprocess
import datetime
import shutil

diretorio='./'
diretorioBack=''
diretorioFront=''
elementos=[]
pastas = os.listdir(diretorio)
for elem in pastas:
    if not os.path.isfile(elem):
        if(("B" in elem) or ("b" in elem)):
            diretorioBack=elem
        if(("F" in elem) or ("f" in elem)):
            diretorioFront=elem
        data=os.listdir(elem)
        elementos.extend(data)
    else:
        if("GPS" in elem):
            elementos.extend([elem])

elementos = sorted(elementos)

tudao=[]

def converteNumero(texto):
    horas = int(int(texto)/10000)
    minutos = int(int(texto) % 10000/100)
    segundos = int(texto) % 100
    return horas*3600+minutos*60+segundos


def comparaData(dataAnterior, dataAtual):
    if (dataAtual == dataAnterior):
        return 1
    else:
        return 0


back = []
front = []
for i in elementos:
    if ("B.mp4" in i):
        back.append(i)
    elif ("F.mp4" in i):
        front.append(i)
    else:
        arquivoGPS = i

concatVetor = []
concatVetor.append(back)
concatVetor.append(front)

caminho_arquivo = f'./{arquivoGPS}'
# Abre o arquivo no modo de leitura
with open(caminho_arquivo, 'r') as arquivo:
    conteudo = arquivo.readlines()

vetAllVideos = []

# Para cada linha do arquivo de gps salva no vetor apenas o nome do vídeo
for line in conteudo:
    subs = line.split(",")
    if (len(subs) > 8):
        # Tirar \n do final da string
        subs[9] = subs[9].replace('\n', '')
        vetAllVideos.append(subs[9])

vetSemVideos = []

# Busca os nomes dispoibilizados pelo GPS que nao possuem video
for video in vetAllVideos:
    if (not video in elementos):
        if (not "F.mp4" in video):
            vetSemVideos.append(video)

# Converte para set para tirar repetição
vetSemVideos = set(vetSemVideos)
vetSemVideos = sorted(list(vetSemVideos))
tudao.append(vetSemVideos)


# Cria o arquivo que contem todos os dados de GPS que nao possuem video
caminho_arquivo = f'./NO-semVideo.txt'
with open(caminho_arquivo, 'w') as arquivo:
    for video in vetSemVideos:
        nomeArquivo = video.replace(".mp4", ".txt")
        arquivo.write('file '+nomeArquivo+'\n')


tempoAnterior = 0
tempoAtual = 0
dataAnterior = 0
dataAtual = 0
confereData = 0

matrizVideos = []


for vetor in concatVetor:
    vetAux = []
    tempoAnterior = 0
    tempoAtual = 0
    dataAnterior = 0
    dataAtual = 0
    confereData = 0

    for i in range(len(vetor)):
        subs = vetor[i].split('-')

        tempoAtual = converteNumero(subs[1])
        dataAtual = subs[0]

        if (tempoAnterior == 0):
            tempoAnterior = tempoAtual
        if (dataAnterior == 0):
            dataAnterior = dataAtual

        confereData = comparaData(dataAnterior, dataAtual)
        diffSegundos = tempoAtual-tempoAnterior

        # Vídeos diferentes
        if ((diffSegundos > 185 or (diffSegundos < 175 and diffSegundos > 0)) or (confereData == 0)):
            if (len(vetAux) > 0):
                matrizVideos.append(vetAux)
                tudao.append(vetAux)
                vetAux = []
                vetAux.append(vetor[i])

        # Vídeo iguais
        else:
            vetAux.append(vetor[i])

        # Ultima iteração do laço
        if (i == (len(vetor)-1)):
            if (len(vetAux) > 0):
                matrizVideos.append(vetAux)
                tudao.append(vetAux)
                vetAux = []

        tempoAnterior = tempoAtual

# for vetor in matrizVideos:
#     nomeArquivo = vetor[0].replace(".mp4", ".txt")
#     caminho_arquivo = f'./{nomeArquivo}'
#     with open(caminho_arquivo, 'w') as arquivo:
#         for elemento in vetor:
#             arquivo.write('file '+elemento+'\n')


# Concatenacao de videos
def concat(arquivoInput,output_file):
    playlist_file='playlist.txt'
    with open(playlist_file,'w') as pFile:
        for file in arquivoInput:
            if("B" in file):
                pFile.write(f"file ./{diretorioBack}/{file}\n")
            else:
                pFile.write(f"file ./{diretorioFront}/{file}\n")

    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', playlist_file, '-c', 'copy', output_file]
    subprocess.run(command)

    # Remover o arquivo de lista de reprodução
    os.remove(playlist_file)


for lista in tudao:
    nome_arquivo=lista[0]
    nome_arquivo=nome_arquivo.split('-')
    if(not 'semVideo' in nome_arquivo[1]):
        if("B" in nome_arquivo[2]):
            nome_arquivo=nome_arquivo[0]+'-'+nome_arquivo[1]+'-Back.mp4'
        else:
            nome_arquivo=nome_arquivo[0]+'-'+nome_arquivo[1]+'-Frnt.mp4'
        concat(lista,nome_arquivo)



def convert_unix_timestamp(unix_timestamp):
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    return dt

def preenchePlanilha(arquivo,dado):
    arquivo.write(dado)


# Buscar arquivo GPS

# Para cada vetor no conjunto de vetores de vídeos
for lista in tudao:
    arquivo=lista[0].replace(".mp4",".csv")
    novoNome=""
    if(not "F" in arquivo):
        with open(arquivo,'w') as gpsFile:            
            for dado in lista:
                for line in conteudo:
                    infosArquivo=line.split(',')        
                    if(len(infosArquivo)>8):
                        if(dado in infosArquivo[9]):
                            if(infosArquivo[1] == "A"):
                                if(novoNome==""):
                                    novoNome=infosArquivo[0]
                                preenchePlanilha(gpsFile,line)
        if(lista[0]==vetSemVideos[0]):
            os.replace(arquivo,'NO-semVideo.csv')
        else:
            data=convert_unix_timestamp(int(novoNome))
            ano='{:04d}'.format(data.year)
            mes='{:02d}'.format(data.month)
            dia='{:02d}'.format(data.day)
            hora='{:02d}'.format(data.hour)
            minuto='{:02d}'.format(data.minute)
            segundo='{:02d}'.format(data.second)
            novoNome=f"NO{ano}{mes}{dia}-{hora}{minuto}{segundo}.csv"                  
            os.replace(arquivo,novoNome)



# Movimentacao


nome_pasta = 'videosConcatenados'
# Verificar se a pasta não existe antes de criar
if not os.path.exists(nome_pasta):
    os.makedirs(nome_pasta)

nome_pasta = 'gpsFiles'
# Verificar se a pasta não existe antes de criar
if not os.path.exists(nome_pasta):
    os.makedirs(nome_pasta)

files=os.listdir('./')
for i in files:
    if os.path.isfile(i):
        if(("NO" in i) and ((".txt" in i) or (".csv" in i))):
            shutil.move(i, 'gpsFiles')
        elif(("NO" in i) and (".mp4" in i)):
            shutil.move(i, 'videosConcatenados')
