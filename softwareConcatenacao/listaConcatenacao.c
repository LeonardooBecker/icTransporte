#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <dirent.h>
#include <getopt.h>

#define MAX_PALAVRA 1024
#define CARACTERE_CAMERA 24
#define QNT_INFOS 3
#define QNT_CAMERAS 2
#define MAX_VIDEOS 1000
#define DIRETORIO 100

void trocaPosicao(char linha[MAX_VIDEOS][MAX_PALAVRA], int atual, int novo)
{
    char aux[MAX_PALAVRA];
    strcpy(aux, linha[atual]);
    strcpy(linha[atual], linha[novo]);
    strcpy(linha[novo], aux);
}

int converteNumero(int valor)
{
    int horas = valor / 10000;
    int minutos = (valor % 10000) / 100;
    int segundos = (valor % 100);
    return horas * 3600 + minutos * 60 + segundos;
}

int main(int argc, char **argv)
{
    int i = 0;
    int j = 0;
    int k = 0;
    int menor;
    char *ptr;
    int vazio = 1;
    FILE *arqResultado;
    char diretorio[MAX_PALAVRA];
    char linha[MAX_VIDEOS][MAX_PALAVRA];
    char linhaBackup[MAX_PALAVRA];
    char nomeArquivo[MAX_PALAVRA];
    char gpsFileName[MAX_PALAVRA];
    char semVideo[MAX_VIDEOS][MAX_PALAVRA];
    char nomeAnterior[MAX_PALAVRA];
    FILE *gpsFile;
    int video = 0;
    int horaAnterior = 0;
    int horaAtual;
    int cont=0;
;    int videosDiferentes = 0;

    int indicaSeparacao[MAX_VIDEOS];

    strcpy(diretorio, argv[1]);

    struct dirent *de;
    DIR *dr = opendir(diretorio);

    if (dr == NULL)
    {
        perror("Erro ao abrir diretório\n");
        exit(1);
    }

    while ((de = readdir(dr)) != NULL)
    {
        if (de->d_type == DT_DIR)
            printf("Diretorio!\n");

        else if (((de->d_name[0]) != 78) && ((de->d_name[1]) != 79))
        {
            strcpy(gpsFileName,diretorio);
            strcat(gpsFileName,"/");
            strcat(gpsFileName,de->d_name);
        }

        // Copia o nome de todos os vídeos existentes no diretório passado para a variavel "linha"

        else if (de->d_type == DT_REG)
        {
            i = 0;
            while (de->d_name[i] != '\0')
            {
                i++;
            }
            // 4 pois esta procurando os arquivos .mp4 ( 4 como último caractere )
            if (de->d_name[(i - 1)] == '4')
            {
                strcpy(linha[video], de->d_name);
                video++;
            }
        }

        else
        {
            perror("Tipo invalido!");
            exit(1);
        }
    }

    // Ordena os vídeos em ordem crescente, para que a junção fique correta

    for (i = 0; i < video; i++)
    {
        menor = i;
        for (j = i; j < video; j++)
        {
            if (strcmp(linha[j], linha[menor]) < 0)
                menor = j;
        }
        trocaPosicao(linha, i, menor);
    }

    // A primeira separação eh o proprio inicio dos arquivos
    indicaSeparacao[0] = 0;
    j = 1;

    /* Verifica se há videos de momentos diferentes dentro da pasta, caso sim guarda a posiçaõ do vídeo de troca */
    for (i = 0; i < video; i++)
    {
        strcpy(linhaBackup, linha[i]);
        ptr = strtok(linhaBackup, "-");
        ptr = strtok(NULL, "-");
        horaAtual = converteNumero(atoi(ptr));
        if (horaAnterior == 0)
            horaAnterior = horaAtual;
        if (abs(horaAtual - horaAnterior) > 185)
        {
            videosDiferentes++;
            indicaSeparacao[j] = i;
            j++;
        }
        horaAnterior = horaAtual;
    }

    gpsFile = fopen(gpsFileName, "r");
    if (!gpsFile)
    {
        perror("Arquivo não encontrado");
        exit(1);
    }
    cont=0;
    while(!feof(gpsFile))
    {
        if (fgets(linhaBackup, MAX_PALAVRA, gpsFile))
        {
            if(strlen(linhaBackup)>10)
            {
                ptr=strtok(linhaBackup,",");
                for(i=0;i<9;i++)
                    ptr=strtok(NULL,",");
                
                if(strcmp(ptr,linha[0])==0)
                    break;
                else
                {
                    //printf("%s",ptr);
                    if(cont==0)
                    {
                        strcpy(semVideo[0],ptr);
                        strcpy(nomeAnterior,ptr);
                        cont++;
                    }
                    else
                    {
                        if(strcmp(ptr,nomeAnterior)!=0)
                        {   
                            strcpy(semVideo[cont],ptr);
                            strcpy(nomeAnterior,ptr);
                            cont++;
                        }
                    }
                }
                
            }
        }
    }
    fclose(gpsFile);
    gpsFile=fopen("NO_semVideo.txt","w");
    if (!gpsFile)
    {
        perror("Arquivo não encontrado");
        exit(1);
    }
    for(i=0;i<cont;i++)
    {
        fprintf(gpsFile,"file %s\n",semVideo[i]);
    }

    while (videosDiferentes >= 0)
    {
        // Laço com duas repetições pois (Back e Front)
        for (i = 0; i < 2; i++)
        {
            vazio = 1;
            horaAnterior = 0;

            /*
                Cria arquivo com o nome do primeiro vídeo da sequencia
            */
            strcpy(linhaBackup, linha[(indicaSeparacao[k])]);
            ptr = strtok(linhaBackup, "-");
            strcpy(nomeArquivo, ptr);
            ptr = strtok(NULL, "-");
            strcat(nomeArquivo, "-");
            strcat(nomeArquivo, ptr);

            if (i == 0)
                strcat(nomeArquivo, "-Back.txt");
            else
                strcat(nomeArquivo, "-Frnt.txt");

            arqResultado = fopen(nomeArquivo, "w");

            if (!arqResultado)
            {
                perror("Erro ao abrir o arquivo!");
                exit(1);
            }

            // Busca em todos os arquivos de video os que devem ser escritos dentro do arquivo aberto atualmente

            for (j = (indicaSeparacao[k]); j < video; j++)
            {

                strcpy(linhaBackup, linha[j]);
                ptr = strtok(linhaBackup, "-");
                ptr = strtok(NULL, "-");
                horaAtual = converteNumero(atoi(ptr));

                if (horaAnterior == 0)
                    horaAnterior = horaAtual;

                // Caso a diferença de tempo seja maior que 3 minutos, quebra o laço partindo para o proximo arquivo
                if ((horaAtual - horaAnterior) > 182)
                    break;

                // Confere se o caractere que diferencia qual das cameras eh igual ao caracter do arquivo resultante aberto atual
                if ((linha[j][24] == 66) && (nomeArquivo[18] == 66))
                {
                    fprintf(arqResultado, "file %s\n", linha[j]);
                    vazio = 0;
                }
                // Confere se o caractere que diferencia qual das cameras eh igual ao caracter do arquivo resultante aberto atual
                else if ((linha[j][24] == 70) && (nomeArquivo[18] == 70))
                {
                    fprintf(arqResultado, "file %s\n", linha[j]);
                    vazio = 0;
                }
                horaAnterior = horaAtual;
            }
            if (vazio)
            {
                remove(nomeArquivo);
            }
            fclose(arqResultado);
        }
        videosDiferentes -= 1;
        k++;
    }
    closedir(dr);
    return 0;
}