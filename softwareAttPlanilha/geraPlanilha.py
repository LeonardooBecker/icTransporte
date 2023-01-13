import pandas as pd
import os
from datetime import date 
import math
import sys
  
def calculateAge(birthDate): 
    days_in_year = 365.2425    
    age = int((date.today() - birthDate).days / days_in_year) 
    return age 

path=sys.argv[1]

for file in os.listdir(path):
    if file.startswith("NDS-BR"):
        planilhaCondut=path+file

dfCondut=pd.read_excel(planilhaCondut)

newDf = (dfCondut.filter(["Driver", "Idade"]))

condutores=[]
idades=[]


for coluna, dados in newDf.iterrows():
    condutor=str(dados[0]).split("_")
    if(len(condutor)>1):
        condutores.append(condutor[1])
    idade=float(dados[1])
    if(not math.isnan(idade)):
        idade=int(idade/10)
        faixa=str(idade*10)+' a '+str(idade*10+9)
        idades.append(faixa)

data={"DRIVER":condutores,"IDADE":idades}

new_df=pd.DataFrame(data)

total=[]

for file in os.listdir(path):
    if file.startswith("Fulltable") and file.endswith(".csv"):
        filename=path+'/'+file
        arquivo=open(filename,'r')
        total.extend((arquivo.readlines()))
        arquivo.close()

escrito=0

arquivo=open("AllFullTable.csv",'w')
for i in total:
    div=i.split(";")

    # Retira o /n para poder adicionar a coluna "IDADES" depois
    div[33]=div[33].replace("\n","")

    # Converte o PICK_UP em 0 quando NPI
    if(div[25]=="NPI"):
        div[25]="0"
    
    # Conversão do VALID_TIME de yes or no para 1 ou 0
    if(div[18]=="Yes" or div[18]=="yes"):
        div[18]="1"
    if(div[18]=="No" or div[18]=="no"):
        div[18]="0"

    # Conversão do WSB de yes or no para 1 ou 0
    if(div[22]=="Yes" or div[22]=="yes" or div[22]=="NPI"):
        div[22]="1"
    if(div[22]=="No" or div[22]=="no"):
        div[22]="0"
    
    # Trocar o separador de vírgula para ponto
    div[14]=div[14].replace(",",".")

    div[1]=div[1].replace(",",".")

    div[2]=div[2].replace(",",".")
    
    # Considera-se o limite NPI como indeterminado, portanto 0 ( limite não específicado )
    if(div[33]=="NPI"):
        div[33]="0"

    if(((div[0]!="DRIVER")  and (div[18]=="1")) or not escrito):
        if not escrito:
            line=div[0]+';'+div[1]+';'+div[2]+';'+div[7]+';'+div[11]+';'+div[12]+';'+div[14]+';'+div[16]+';'+div[18]+';'+div[19]+';'+div[22]+';'+div[23]+';'+div[24]+';'+div[25]+';'+div[26]+';'+div[28]+';'+div[29]+';'+div[31]+';'+div[32]+';'+div[33]+';'+"IDADE\n"
        else:
            condutor=str(div[0])
            dfFiltro=new_df[new_df["DRIVER"]==condutor]
            idade=dfFiltro["IDADE"].iloc[0]
            line=div[0]+';'+div[1]+';'+div[2]+';'+div[7]+';'+div[11]+';'+div[12]+';'+div[14]+';'+div[16]+';'+div[18]+';'+div[19]+';'+div[22]+';'+div[23]+';'+div[24]+';'+div[25]+';'+div[26]+';'+div[28]+';'+div[29]+';'+div[31]+';'+div[32]+';'+div[33]+';'+str(idade)+'\n'
        arquivo.write(line)
        escrito=1
arquivo.close()