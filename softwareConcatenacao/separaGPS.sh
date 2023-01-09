#/bin/bash
CONDUTOR=$1
DIR=$2

valorAntigo=0
valorAtual=0

var2=$(find $DIR -maxdepth 1 | grep "GPS" | grep ".txt" )

gcc -Wall geraPlanilha.c -o geraPlanilha

if [ -z "$var2" ]; then
    echo "Arquivo de GPS não encontrado"
else
    echo $var2
fi

# Busca todos os arquivos gerados pelo programa listaConcatenacao.c
for arq in $(find $DIR -maxdepth 1 | grep "NO" | grep ".txt" );
do
    # Para cada arquivo encontrado, faz a leitura de todas as linhas existentes dentro dele
    for linha in $(cat $arq);
    do
        #Condição necessária pois o cat separa a palavra file do restante da linha que contem o nome do arquivo
        if [ "$linha" != "file" ]; then
            arquivo=$(echo $arq | cut -d/ -f2 | cut -c 3-17) # Linha responsáve por cortar parte do nome do arquivo, deixando mais limpo o nome do arquivo de texto/csv gerado
            echo $(cat $var2 | grep "$linha" ) >> Dados$arquivo.txt
        fi
    done
    tr -s '[:space:]' '\n' < Dados$arquivo.txt > arquivoAuxiliar # Retira todos os espaços no começo de cada linha
    mv arquivoAuxiliar Dados$arquivo.txt
    echo $arquivo
    ./geraPlanilha $CONDUTOR Dados$arquivo.txt

    # var3=$(find ./ -maxdepth 1 | grep novoNome | cut -d= -f2) # Procura os arquivos que contem o novo nome a ser dado as planilhas geradas anteriormente
    # mv Dados$arquivo.csv $var3 # Renomeia as planilhas para o novo nome
    # rm novoNome*
done	

if [ ! -d "gpsFiles" ]; then
    mkdir gpsFiles
fi
mv Dados* gpsFiles
