#/bin/bash
DIR=$1
var1=$(ls $DIR/*.txt | cut -c 10-31)
echo $var1
for arq in $(find $DIR -maxdepth 1 | grep "NO202" | grep ".txt" );
do
	echo $arq
	var2=$(echo $arq | cut -d/ -f2 | cut -c 3-22)Full.mp4
	ffmpeg -f concat -safe 0 -i $arq -c copy $var2	
done	
