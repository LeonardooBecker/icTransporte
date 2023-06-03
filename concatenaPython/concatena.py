import os
import subprocess
import datetime
import shutil
import sys

diretorio = './'
diretorioBack = ''
diretorioFront = ''
elementos = []
pastas = os.listdir(diretorio)
for elem in pastas:
    if not os.path.isfile(elem):
        if (("B" in elem) or ("b" in elem)):
            diretorioBack = elem
        if (("F" in elem) or ("f" in elem)):
            diretorioFront = elem
        data = os.listdir(elem)
        elementos.extend(data)
    else:
        if ("GPS" in elem):
            elementos.extend([elem])

elementos = sorted(elementos)

tudao = []


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
    elif ("GPS" in i):
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
# caminho_arquivo = f'./NO-semVideo.txt'
# with open(caminho_arquivo, 'w') as arquivo:
#     for video in vetSemVideos:
#         nomeArquivo = video.replace(".mp4", ".txt")
#         arquivo.write('file '+nomeArquivo+'\n')


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

# Cria o arquivo que contem todos os dados de GPS que possuem video
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


def toDict(datetime):
    data = {'ano': None, 'mes': None, 'dia': None,
            'hora': None, 'minuto': None, 'segundo': None}
    data['ano'] = '{:04d}'.format(datetime.year)
    data['mes'] = '{:02d}'.format(datetime.month)
    data['dia'] = '{:02d}'.format(datetime.day)
    data['hora'] = '{:02d}'.format(datetime.hour)
    data['minuto'] = '{:02d}'.format(datetime.minute)
    data['segundo'] = '{:02d}'.format(datetime.second)
    return data


def algo(texto, info):
    if (texto == 'latitude'):
        info[3] = str(info[3])
        return (info[3].replace('.', ','))
    if (texto == 'longitude'):
        info[2] = str(info[2])
        return (info[2].replace('.', ','))
    if (texto == 'dia'):
        data = convert_unix_timestamp(int(info[0]))
        data = toDict(data)
        return data['dia']+'/'+data['mes']+'/'+data['ano']
    if (texto == 'hora'):
        data = convert_unix_timestamp(int(info[0]))
        data = toDict(data)
        return data['hora']+':'+data['minuto']+':'+data['segundo']
    if (texto == 'velocidadeKMH'):
        vel = int(info[5])*3.6/100
        vel = str('{:05f}'.format(vel))
        return vel
    if (texto == 'velocidadeMPH'):
        vel = int(info[5])*3.6/100/1.609
        vel = str('{:05f}'.format(vel))
        return vel


def preencheVetor(matriz, dado):
    vetor = []
    diffSegundos = 0
    aceleracao = 0
    columData = dado.split(',')
    timeAcum = 0
    if (len(matriz) > 1):
        horaAnterior = matriz[(len(matriz)-1)][8]
        horaAnterior = horaAnterior.replace(':', '')
        horaAnterior = converteNumero(horaAnterior)
        horaAtual = columData[0]
        data = convert_unix_timestamp(int(horaAtual))
        data = toDict(data)
        horaAtual = data['hora']+data['minuto']+data['segundo']
        horaAtual = converteNumero(horaAtual)
        diffSegundos = horaAtual-horaAnterior

        velocidadeAnterior = float(
            matriz[(len(matriz)-1)][14].replace(',', '.'))
        velocidadeAtual = float(algo('velocidadeKMH', columData))
        diffVelocidade = velocidadeAtual-velocidadeAnterior
        if (diffSegundos > 0):
            aceleracao = '{:05f}'.format(diffVelocidade/diffSegundos)
        else:
            aceleracao = 0
        # Elimina linha repetidas
        if (diffSegundos == 0):
            return

    # Chamada recursiva para preencher linha faltante
    if (diffSegundos == 2):
        columData[0] = str(int(columData[0])-1)
        timeAcum
        dd = ','.join(columData)
        preencheVetor(matriz, dd)
        columData[0] = str(int(columData[0])+1)
        diffSegundos = 1
    if (diffSegundos > 2 or diffSegundos < 0):
        diffSegundos = 1

    argumentos = sys.argv
    # DRIVE
    vetor.append(argumentos[1])
    # LONG
    vetor.append(algo('longitude', columData))
    # LAT
    vetor.append(algo('latitude', columData))
    # DAY
    vetor.append('')
    # DAYCORRIGIDO
    vetor.append(algo('dia', columData))
    # 03:00:00
    vetor.append('')
    # TRIP
    vetor.append('')
    # ID
    vetor.append(argumentos[1])
    # PR
    vetor.append(algo('hora', columData))
    # H
    vetor.append('')
    # M
    vetor.append('')
    # S
    vetor.append(diffSegundos)
    # TIME ACUM
    if (len(matriz) > 1):
        if (diffSegundos <= 3):
            timeAcum = matriz[(len(matriz)-1)][12]+diffSegundos
        else:
            timeAcum = matriz[(len(matriz)-1)][12]+1
    vetor.append(timeAcum)
    # SPD_MPH
    vetor.append(str(algo('velocidadeMPH', columData)).replace('.', ','))
    # SPD_KMH
    vetor.append(str(algo('velocidadeKMH', columData)).replace('.', ','))
    # ACEL_MS2
    vetor.append(str(aceleracao).replace('.', ','))
    # HEADING
    vetor.append('')
    # ALTITUDE
    vetor.append('')
    # VALID_TIME
    vetor.append('')
    # TIMESTAMP
    vetor.append('')
    # CPOOL
    vetor.append('')
    # CPOOLING
    vetor.append('')
    # WSB
    vetor.append('')
    # UMP_YN
    vetor.append('')
    # UMP
    vetor.append('')
    # PICK_UP
    vetor.append('')
    # ACTION
    vetor.append('')
    # GPS_FILE
    vetor.append(columData[9])
    # CIDADE
    vetor.append('')
    # BAIRRO
    vetor.append('')
    # NOME_RUA
    vetor.append('')
    # HIERARQUIA_CWB
    vetor.append('')
    # HIERARQUE_CTB
    vetor.append('')
    # LIMITE_VEL
    vetor.append('')
    vetor.append('\n')
    matriz.append(vetor)


def colum_names(matriz):
    vetor = []
    vetor.append('DRIVER')
    vetor.append('LONG')
    vetor.append('LAT')
    vetor.append('DAY')
    vetor.append('DAY_CORRIGIDO')
    vetor.append('03:00:00')
    vetor.append('TRIP')
    vetor.append('ID')
    vetor.append('PR')
    vetor.append('H')
    vetor.append('M')
    vetor.append('S')
    vetor.append('TIME_ACUM')
    vetor.append('SPD_MPH')
    vetor.append('SPD_KMH')
    vetor.append('ACEL_MS2')
    vetor.append('HEADING')
    vetor.append('ALTITUDE_FT')
    vetor.append('VALID_TIME')
    vetor.append('TIMESTAMP')
    vetor.append('CPOOL')
    vetor.append('CPOOLING')
    vetor.append('WSB')
    vetor.append('UMP_YN')
    vetor.append('UMP')
    vetor.append('PICK_UP')
    vetor.append('ACTION')
    vetor.append('GPS_FILE')
    vetor.append('CIDADE')
    vetor.append('BAIRRO')
    vetor.append('NOME_RUA')
    vetor.append('HIERARQUIA_CWB')
    vetor.append('HIERARQUIA_CTB')
    vetor.append('LIMITE_VEL')
    vetor.append('\n')
    matriz.append(vetor)


def preenchePlanilha(arquivo, matriz):
    for i in matriz:
        for dado in i:
            if (dado != '\n'):
                arquivo.write(str(dado)+';')
            else:
                arquivo.write(str(dado))


# Buscar arquivo GPS

# Para cada vetor no conjunto de vetores de vídeos
for lista in tudao:
    matriz = []
    colum_names(matriz)
    arquivo = lista[0].replace(".mp4", ".csv")
    novoNome = ""
    if (not "F" in arquivo):
        with open(arquivo, 'w') as gpsFile:
            for dado in lista:
                for line in conteudo:
                    infosArquivo = line.split(',')
                    if (len(infosArquivo) > 8):
                        if (dado in infosArquivo[9]):
                            if (infosArquivo[1] == "A"):
                                if (novoNome == ""):
                                    novoNome = infosArquivo[0]
                                vetor = []
                                preencheVetor(matriz, line)
            preenchePlanilha(gpsFile, matriz)

        if (lista[0] == vetSemVideos[0]):
            os.replace(arquivo, 'NO-semVideo.csv')
        else:
            data = convert_unix_timestamp(int(novoNome))
            data = toDict(data)
            print(arquivo)
            novoNome = f"NO{data['ano']}{data['mes']}{data['dia']}-{arquivo.split('-')[1]}-{data['hora']}{data['minuto']}{data['segundo']}.csv"
            os.replace(arquivo, novoNome)


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
