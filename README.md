# Estudo Naturalístico de Direção Brasileira


### Repositório que contém os softwares desenvolvidos para conversão de dados adquiridos pelas câmeras 70mai A800, e adequação das planilhas para apresentação no site [Painel NDS BR](https://painelndsbr.streamlit.app/) hospedado pelo streamlit.


#### -SoftwareConcatenacao

Softwares desenvolvidos nas linguagens C e Python. Para correta execução, é necessário incluir dentro do diretório ( contendo os arquivos do software ), uma pasta com os vídeos a serem concatenados  e o arquivo de GPS disponibilizado pela câmera 70mai A800.  
Para executar o programa basta digitar no terminal:  
~~~Bash
./processaDados.sh “Condutor” “Pasta”
~~~
_Do qual:   
“Condutor” é o condutor responsável por gerar as gravações;   
“Pasta” é a pasta em que foram adicionados os arquivos anteriormente descritos._

#### -SoftwareAttPlanilha:

Software desenvolvido em Python. Para correta execução, é necessário ter uma pasta contendo as planilhas completas de dados “FullTable” ( **formato .csv** ), e a planilha de cadastro dos condutores “NDS-BR_CadastroCondutores” ( **formato .xlxs** ).  
Para executar o programa basta digitar no terminal:  
~~~python
python3 geraPlanilha.py "pasta"
~~~
_Do qual "pasta" é o nome da pasta onde foram inseridos os arquivos anteriormente descritos._


