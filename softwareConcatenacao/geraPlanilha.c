#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_PALAVRA 1024
#define QNT_CAMPOS 13

// Struct que contem informações para cada coluna da planilha
struct dados
{
    int tempoAnteriorUTC;
    int tempoAtualUTC;
    double latitude;
    double longitude;
    double velocidadeAnterior;
    double velocidadeKmh;
    double velocidadeMph;
    double diffVelocidade;
    double aceleracao;
    char nomeArquivo[MAX_PALAVRA];
    char tempoCompleto[MAX_PALAVRA];
    char ID[MAX_PALAVRA];
    char *trip;
    char horario[MAX_PALAVRA];
    int soma_acumulada;
    char *altitude;
    char condutor[MAX_PALAVRA];
    char day_corrigido;
    int mes, dia, ano;
    int segundos, hora, minutos;
    int diffSegundos;
};
typedef struct dados dados_t;

// Retorna a string mês no valor correspondente
int converteMes(char *mes)
{
    if (!(strcmp(mes, "Jan")))
        return 1;
    if (!(strcmp(mes, "Feb")))
        return 2;
    if (!(strcmp(mes, "Mar")))
        return 3;
    if (!(strcmp(mes, "Apr")))
        return 4;
    if (!(strcmp(mes, "May")))
        return 5;
    if (!(strcmp(mes, "Jun")))
        return 6;
    if (!(strcmp(mes, "Jul")))
        return 7;
    if (!(strcmp(mes, "Aug")))
        return 8;
    if (!(strcmp(mes, "Sep")))
        return 9;
    if (!(strcmp(mes, "Oct")))
        return 10;
    if (!(strcmp(mes, "Nov")))
        return 11;
    if (!(strcmp(mes, "Dec")))
        return 12;
    return 0;
}

// Distruibui os valores registrados dentro da matriz campo, para cada elemento da struct
void distribuiParametrosTXT(dados_t *infos, char campo[QNT_CAMPOS][MAX_PALAVRA])
{
    time_t curtime;
    char tempo[MAX_PALAVRA];
    /* funcao que retorna o horario referente aos segundos UTC passado para ele */
    curtime = atoi(campo[0]);
    strcpy(tempo, ctime(&curtime));

    /* Substitui o último caractere da string tempo. ( Anteriormente era um /n e após isso passa a ser um espaço vazio ) */
    tempo[((strlen(tempo)) - 1)] = 0;

    strcpy(infos->tempoCompleto, tempo);
    strcpy(infos->nomeArquivo, campo[9]);
    infos->latitude = atof(campo[2]);
    infos->longitude = atof(campo[3]);
    infos->velocidadeKmh = atof(campo[5]) * 3.6 / 100;
    infos->velocidadeMph = infos->velocidadeKmh / 1.609;
}

// Retorna os segundos do horario
int devolveSegundos(dados_t info)
{
    char *pt;
    pt = strtok(info.horario, ":");
    pt = strtok(NULL, ":");
    pt = strtok(NULL, ":");
    return atoi(pt);
}

// Retorna os minutos do horario
int devolveMinutos(dados_t info)
{
    char *pt;
    pt = strtok(info.horario, ":");
    pt = strtok(NULL, ":");
    return atoi(pt);
}

// Retorna as horas do horario
int devolveHoras(dados_t info)
{
    char *pt;
    pt = strtok(info.horario, ":");
    return atoi(pt);
}

// Função responsável por definir parâmetros da struct infos, a partir da quebra da string contida em tempoCompleto
void cortaHorario(dados_t *infos)
{
    char *pt;
    // Corta a string de forma que seja possível coletar o mes
    pt = strtok(infos->tempoCompleto, " ");
    pt = strtok(NULL, " ");
    infos->mes = converteMes(pt);

    // Corta a string de forma que seja possível coletar o dia
    pt = strtok(NULL, " ");
    infos->dia = atoi(pt);

    // Corta a string de forma que seja possivel coletar o horario completo
    pt = strtok(NULL, " ");
    strcpy(infos->horario, pt);

    // Corta a string de forma que seja possivel coletar o ano
    pt = strtok(NULL, " ");
    infos->ano = atoi(pt);

    infos->segundos = devolveSegundos(*infos);
    infos->minutos = devolveMinutos(*infos);
    infos->hora = devolveHoras(*infos);
}

// Inicializa a primeira linha da coluna com todos os nomes gerais que devem conter nela
void inicializaTabela(FILE *arqResul)
{
    // Driver
    fprintf(arqResul, "DRIVER;");
    // Longitude
    fprintf(arqResul, "LONG;");
    // Latitude
    fprintf(arqResul, "LAT;");
    // Dia
    fprintf(arqResul, "DAY;");
    // Dia corrigido
    fprintf(arqResul, "DAY_CORRIGIDO;");
    // 03:00:00
    fprintf(arqResul, "03:00:00;");
    // Trip
    fprintf(arqResul, "TRIP;");
    // Concatenação AG
    fprintf(arqResul, "ID;");
    // PR
    fprintf(arqResul, "PR;");
    // Hora
    fprintf(arqResul, "H;");
    // Minuto
    fprintf(arqResul, "M;");
    // Segundo
    fprintf(arqResul, "S;");
    // Tempo acumulado
    fprintf(arqResul, "TIME_ACUM;");
    // Spd_mph
    fprintf(arqResul, "SPD_MPH;");
    // Spd_kmh
    fprintf(arqResul, "SPD_KMH;");
    // ACEL_MS2
    fprintf(arqResul, "ACEL_MS2;");
    // HEADING
    fprintf(arqResul, "HEADING;");
    // ALTITUDE-FT
    fprintf(arqResul, "ALTITUDE_FT;");
    // VALID_TIME
    fprintf(arqResul, "VALID_TIME;");
    // TIMESTAMP_GPS
    fprintf(arqResul, "TIMESTAMP_GPS;");
    // CPOOL
    fprintf(arqResul, "CPOOL;");
    // CPOOLING_CHECKED
    fprintf(arqResul, "CPOOLING_CHECK;");
    // WSB
    fprintf(arqResul, "WSB;");
    // UMP_YN
    fprintf(arqResul, "UMP_YN;");
    // UMP
    fprintf(arqResul, "UMP;");
    // PICK_UP
    fprintf(arqResul, "PICK_UP;");
    // ACTION
    fprintf(arqResul, "ACTION;");
    // GPS_FILE
    fprintf(arqResul, "GPS_FILE;");
    // CIDADE
    fprintf(arqResul, "CIDADE;");
    // BAIRRO
    fprintf(arqResul, "BAIRRO;");
    // NOME_RUA
    fprintf(arqResul, "NOME_RUA;");
    // HIERARQUIA_CWB
    fprintf(arqResul, "HIERARQUIA_CWB;");
    // HIERARQUIA_CTB
    fprintf(arqResul, "HIERARQUIA_CTB;");
    // LIMITE_VEL
    fprintf(arqResul, "LIMITE_VEL\n");
}

char *trocaPontoVirgula(float dado) {
    char *str=malloc(sizeof(char)*MAX_PALAVRA);
    sprintf(str,"%f",dado);
    for (int i = 0; i < strlen(str); i++) {
        if (str[i] == '.') {
            str[i] = ',';
        }
    }
    return str;
}

// Função chamada a cada repetição do laço  que preenche a planilha com os dados obtidos
void escrevePlanilha(dados_t infos, FILE *arqResul)
{
    char valorAux[MAX_PALAVRA];
    fprintf(arqResul, "%s;", infos.condutor);                          // DRIVER
    fprintf(arqResul, "%s;", trocaPontoVirgula(infos.longitude));                         // LONGITUDE
    fprintf(arqResul, "%s;", trocaPontoVirgula(infos.latitude));                          // LATITUDE
    fprintf(arqResul, ";");                                            // DAY
    fprintf(arqResul, "%d/%02d/%d;", infos.dia, infos.mes, infos.ano); // DAY CORRIGIDO
    fprintf(arqResul, ";");                                            // 03:00:00
    fprintf(arqResul, "%s;", infos.trip);                              // TRIP
    fprintf(arqResul, "%s;", infos.ID);                                // ID
    fprintf(arqResul, "%s;", infos.horario);                           // PR
    fprintf(arqResul, ";");                                            // H
    fprintf(arqResul, ";");                                            // M
    fprintf(arqResul, "%d;", infos.diffSegundos);                      // S
    fprintf(arqResul, "%d;", infos.soma_acumulada);                    // TIME_ACUM
    fprintf(arqResul, "%s;", trocaPontoVirgula(infos.velocidadeMph));                   // SPD_MPH
    fprintf(arqResul, "%s;", trocaPontoVirgula(infos.velocidadeKmh));                   // SPM_KMH
    fprintf(arqResul, "%s;", trocaPontoVirgula(infos.aceleracao / 3.6));                // ACEL_MS2
    fprintf(arqResul, ";");                                            // HEADING
    fprintf(arqResul, "%s;", infos.altitude);                          // ALTITUDE
    fprintf(arqResul, " ; ; ; ; ; ; ; ; ;");
    fprintf(arqResul, "%s", infos.nomeArquivo);
    fprintf(arqResul, " ; ; ; ; ; ;");
    // fprintf(arqResul, "%s;", infos.tempoCompleto);
    // fprintf(arqResul, "%s", infos.nomeArquivo);
    fprintf(arqResul, "\n");
}

int main(int argc, char **argv)
{
    FILE *arqEntrada;
    FILE *arqResul;
    char result[MAX_PALAVRA * 2];
    char arquivo[MAX_PALAVRA];
    char linha[MAX_PALAVRA];
    char campo[QNT_CAMPOS][MAX_PALAVRA];
    char *pt;
    int i;
    int aberto = 0;
    dados_t infos;

    infos.tempoAnteriorUTC = 0;
    infos.diffSegundos = 0;
    infos.diffVelocidade = 0;
    infos.velocidadeAnterior = 0;

    strcpy(infos.condutor, argv[1]);
    strcpy(arquivo, argv[2]);

    infos.trip = "";
    infos.altitude = "";

    arqEntrada = fopen(arquivo, "r");
    if (!arqEntrada)
    {
        perror("Arquivo não encontrado");
        exit(1);
    }

    while (!feof(arqEntrada))
    {
        i = 1;
        if (fgets(linha, MAX_PALAVRA, arqEntrada))
        {
            pt = strtok(linha, ",");
            strcpy(campo[0], pt);
            while (pt)
            {
                pt = strtok(NULL, ",");
                if (pt == NULL)
                    break;
                strcpy(campo[i], pt);
                i++;
            }
        }

        distribuiParametrosTXT(&infos, campo); // Pega os dados coletados a cada linha do arquivo TXT e distribui para os parametros da struct

        cortaHorario(&infos); // Divide a string contida em tempo completo da struct em outros parametros utilizados posteriormente

        infos.tempoAtualUTC = atoi(campo[0]);

        if ((infos.tempoAnteriorUTC != 1609430400) && (infos.tempoAnteriorUTC != 0))
        {
            infos.diffSegundos = infos.tempoAtualUTC - infos.tempoAnteriorUTC;
            infos.diffVelocidade = infos.velocidadeKmh - infos.velocidadeAnterior;
        }
        infos.soma_acumulada += infos.diffSegundos;
        if (infos.diffSegundos != 0)
            infos.aceleracao = infos.diffVelocidade / infos.diffSegundos;

        strcpy(infos.ID, infos.condutor);
        strcat(infos.ID, infos.trip);

        if (infos.tempoAtualUTC != 1609430400)
        {
            if (!aberto)
            {
                /* Utilizado para coletar somente o nome do arquivo, alterando em sequencia o formato de .txt para .csv */
                strtok(arquivo, ".");
                sprintf(result, "%s-%02d%02d%02d.csv", strtok(arquivo, "-"), infos.hora, infos.minutos, infos.segundos);
                arqResul = fopen(result, "w");
                if (!arqResul)
                {
                    perror("Arquivo não encontrado");
                    exit(1);
                }
                inicializaTabela(arqResul);
                aberto = 1;
            }
            escrevePlanilha(infos, arqResul);
        }
        infos.tempoAnteriorUTC = infos.tempoAtualUTC;
        infos.velocidadeAnterior = infos.velocidadeKmh;
    }
    fclose(arqEntrada);
    // Caso exista algum dado na planilha, o arquivo conseguiu ser aberto e houve a inserção de dados
    if (arqResul)
        fclose(arqResul);
    // Caso contrario abre um arquivo com o próprio nome do txt, para fins de melhor identificação
    else
    {
        sprintf(arquivo, "%s.csv", strtok(arquivo, "."));
        arqResul = fopen(arquivo, "w");
        if (!arqResul)
        {
            perror("Arquivo não encontrado");
            exit(1);
        }
        inicializaTabela(arqResul);
        fclose(arqResul);
    }
    return 0;
}
