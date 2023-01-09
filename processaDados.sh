#/bin/bash
CONDUTOR=$1
ENTRADA=$2

gcc -Wall listaConcatenacao.c -o listaConcatenacao

./listaConcatenacao $ENTRADA
mv *.txt ./$ENTRADA
./concatenaVideos.sh $ENTRADA

if [ ! -d "videosConcatenados" ]; then
    mkdir videosConcatenados
fi
mv ./*.mp4 ./videosConcatenados

./separaGPS.sh $CONDUTOR $ENTRADA