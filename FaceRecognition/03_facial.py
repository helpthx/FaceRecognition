''''
Real Time Face Recogition
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    
Developed by João Vitor Rodrigues Baptista  
'''

import cv2
import numpy as np
import os 
import time
from datetime import datetime
import sqlite3
import sys
        
'''
 Para para acessar o database e o dataset atraves de conversão de valores para listas
'''

def convert_list():
        id_list = []
        name_list = []
        matricula_list = []
        ru_list = []
        acessos_list = []
        data = []
        conn = sqlite3.connect('Banco_de_dados.db')
        print ('Database open successfully...');

        cursor = conn.execute("SELECT ID, NOME, MATRICULA, RU, ACESSOS from CADASTROS")
        for row in cursor:
            id_list.append(int(row[0]))
            name_list.append(row[1])
            matricula_list.append(int(row[2]))
            ru_list.append(float(row[3]))
            acessos_list.append(int(row[4]))

        print("Operação feita com sucesso...");
        conn.close()



convert_list()
#Zerar todos os acessos    

conn = sqlite3.connect('Banco_de_dados.db')
print('\nBanco aberto com sucesso...');
print('---------------------------')
        
conn.execute('UPDATE CADASTROS set ACESSOS = 0');
conn.commit()
print('Numero total de colunas atualizadas: ', conn.total_changes)
if conn.total_changes > 0:
    print('Alterado com sucesso...')
else:
    print('Alguma operação deu errado...')

print('\n')
conn.close()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#Contador inicial
id = 0

# Iniciar e começa a video captura de tempo-real
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Definir o tamanho minino do quadrado que será usado para reconhecer o rosto
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

#Inicia a interface grafica de acompanhamento


#Variaveis de temporalização e confirmação de faces
t = 0
v = 0

#Loop principal da aplicação.
while True:
   
    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        
        #atualização real-time do banco
        id_list = []
        name_list = []
        matricula_list = []
        ru_list = []
        acessos_list = []
        data = []
        conn = sqlite3.connect('Banco_de_dados.db')
       
        cursor = conn.execute("SELECT ID, NOME, MATRICULA, RU, ACESSOS from CADASTROS")
        for row in cursor:
            id_list.append(int(row[0]))
            name_list.append(row[1])
            matricula_list.append(int(row[2]))
            ru_list.append(float(row[3]))
            acessos_list.append(int(row[4]))

        conn.close()   
        
        # Iniciação do retangulo de reconhecimento 
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
    # Sistema de valiação por 10 frames não consecutivos    
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 32): #confiabilidade de 68% em cada match de imagem
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            
            #conversão de valores do banco para a aplicação
            nome = name_list[id]
            numb_acessos = acessos_list[id]
            credito = ru_list[id]
            matricula = str(matricula_list[id])
            credito_1 = round(credito - 5.20, 2)
            dinheiro = str(credito_1)
            id = matricula_list[id]
            confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id = 'Acesso permitido'
            iniciar = 1
            sem_credito = 0
            numero_acessos = numb_acessos
            v = v + 1
            
            #condição em que o usuario terá acesso ao restaurante
            if (t == 13 and credito_1 >= 0.0 and numero_acessos == 0):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id = 'Acesso permitido'
                iniciar = 1
                sem_credito = 0
                numero_acessos = 0
                
                                
                #Temporalização para travar a tela de monitoramento e abrir o GPIO da placa
                if(v == 15):
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #Verde
                    id = 'Acesso permitido'
                                                           
                    #Printar no console as informações que serão gravas como logs
                    print('Bem Vindo ', nome)
                    print('Matricula: ', matricula)
                    print('Creditos restantes: ', credito_1)
                    print('\n')
                    
                    #Atualização do banco de dados
                    conn = sqlite3.connect('Banco_de_dados.db')
                    conn.execute("UPDATE CADASTROS set RU = " +str(round(credito_1, 2))+ " WHERE  MATRICULA = "+ str(matricula));
                    conn.execute('UPDATE CADASTROS set ACESSOS = ACESSOS+1 WHERE  MATRICULA='+str(matricula));
                    conn.commit()
                    print('\nNumero total de colunas atualizadas: ', conn.total_changes)
                    if conn.total_changes > 0:
                            print('Alterado com sucesso...')
                    else:
                            print('Alguma operação deu errado...')

                    print('\n')
                    conn.close()
                    
                    #Criando o arquivo de logs
                    now = datetime.now()
                    arq = open('Logs/log.txt', 'a')
                    data = []
                    data.append('\n-------------------------\n')
                    data.append("Data: ")
                    data.append(str(now.year))
                    data.append(':')
                    data.append(str(now.month))
                    data.append(':')
                    data.append(str(now.day))
                    data.append(':')
                    data.append(str(now.hour))
                    data.append(':')
                    data.append(str(now.minute))
                    data.append(':')
                    data.append(str(now.second))
                    data.append(str('\nBem vindo: '+nome))
                    data.append(str('\nMatricula: '+matricula))
                    data.append('\nCreditos restantes: '+str(credito_1))
                    data.append('\nCreditos antes: '+str(credito))
                    data.append('\n------------------------\n')
                    arq.writelines(data)
                    arq.close()

                                      
                    
                    #Abertura do rele
                    time.sleep(5)
                    #os.system("sudo ./gpio")
                    t = 0
                    v = 0
                    time.sleep(0.1)
            
            #Condição em que o usuario não terá creditos suficientes para acessar o restaurante.
            elif(t == 13 and credito_1 < 0.0):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2) #Vermelho
                id = 'Sem creditos...'
                                
                #Temporalização para travar a tela de monitoramento
                if(v == 15):
                    
                    #Printar no console as informações que serão gravas como logs
                    print('Sem saldo ', nome)
                    print('Matricula: ', matricula)
                    print('Creditos restantes: ', credito_1)
                    print('Creditos antes: ', credito)
                    print('\n')
                    
                    #Criando o arquivo de logs
                    now = datetime.now()
                    arq = open('Logs/log.txt', 'a')
                    data = []
                    data.append('\n-------------------------\n')
                    data.append("Data: ")
                    data.append(str(now.year))
                    data.append(':')
                    data.append(str(now.month))
                    data.append(':')
                    data.append(str(now.day))
                    data.append(':')
                    data.append(str(now.hour))
                    data.append(':')
                    data.append(str(now.minute))
                    data.append(':')
                    data.append(str(now.second))
                    data.append(str('\nBem vindo: '+nome))
                    data.append(str('\nMatricula: '+matricula))
                    data.append('\nCreditos restantes: '+str(credito_1))
                    data.append('\nCreditos antes: '+str(credito))
                    data.append('\n------------------------\n')
                    arq.writelines(data)
                    arq.close()
                    
                    #tempo de permanencia da tela de monitoramento 
                    time.sleep(0.1)
                    t = 0
                    v = 0
                    time.sleep(5)
            
            #Condição em que o usuario tentou acessar mais vezes que o permitido no restaurante.
            elif(t == 13 and numero_acessos != 0):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,165,255), 2) #laranjado
                id = 'Numeros de acessos expirados..'
                                
                #Temporalização para travar a tela de monitoramento
                if(v == 15):
                    
                    #Printar no console as informações que serão gravas como logs
                    print('Numeros de acessos expirados... ', nome)
                    print('Matricula: ', matricula)
                    print('\n')
                    
                    #Criando o arquivo de logs
                    now = datetime.now()
                    arq = open('Logs/log.txt', 'a')
                    data = []
                    data.append('\n-------------------------\n')
                    data.append("Data: ")
                    data.append(str(now.year))
                    data.append(':')
                    data.append(str(now.month))
                    data.append(':')
                    data.append(str(now.day))
                    data.append(':')
                    data.append(str(now.hour))
                    data.append(':')
                    data.append(str(now.minute))
                    data.append(':')
                    data.append(str(now.second))
                    data.append('\nNumeros de acessos expirados..')
                    data.append(str('\nNome '+nome))
                    data.append(str('\nMatricula: '+matricula))
                    #data.append('\nCreditos restantes: '+str(credito_1))
                    data.append('\nCreditos: '+str(credito))
                    data.append('\n------------------------\n')
                    arq.writelines(data)
                    arq.close()
                    
                    #tempo de permanencia da tela de monitoramento 
                    time.sleep(5)
                    t = 0
                    v = 0
                    time.sleep(0.1)
                    
            #Condição de incremento de identificação        
            else:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,255), 2) #Amarelo
                id = 'Identificando rosto...'
                #confidence = "  {0}%".format(round(100 - confidence))
                t = t + 1
                
        #confiabilidade menor do que 68% em cada match de imagem       
        elif (confidence < 68):
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            id = 'Desconhecido'
            confidence = "  {0}%".format(round(100 - confidence))
            #t = 0
            #v = 0
        
        #error de frame e resete da interface de monitoramento.
        else:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
            id = 'Erro de captura'
            confidence = "  {0}%".format(round(100 - confidence))
            t = 0
            v = 0
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Limpar as telas quando sair

cam.release()
cv2.destroyAllWindows()
