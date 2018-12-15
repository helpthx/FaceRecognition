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
from fuctions import Real_time_fuctions

c = Real_time_fuctions()

#Working with the local database
c.convert_list()
c.zero_reset()

# % Confidence
const = 100
confidence_in = const - 70 #Up to 70% will have acess
confidence_out = const - confidence_in

#Frames security system
Frames = 13
Frames2 = Frames + 2


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#Inicial account
id = 0

#Init real time video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

#Define smallest square for wich face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)


#Varibles for security increment
Value_Increment1 = 0
Value_Increment2 = 0

#Main application loop
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
        
        #Updating database in real time
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

        #Init rectangle aroud faces
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < confidence_in): #Up to 68% of confidence
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            
            #real time converting values from list
            nome = name_list[id]
            numb_acessos = acessos_list[id]
            credito = ru_list[id]
            matricula = str(matricula_list[id])
            credito_1 = round(credito - 5.20, 2)
            dinheiro = str(credito_1)
            id = matricula_list[id]
            confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id = 'Access Allow'
            iniciar = 1
            sem_credito = 0
            numero_acessos = numb_acessos
            Value_Increment2 = Value_Increment2 + 1
            
            #Condition with acess
            if (Value_Increment1 == Frames and credito_1 >= 0.0 and numero_acessos == 0):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id = 'Access Allow'
                iniciar = 1
                sem_credito = 0
                numero_acessos = 0
                
                                

                if(Value_Increment2 == Frames2):
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #Green
                    id = 'Access Allow'
                                                           
                    #Show in console infos
                    print('Welcome: ', nome)
                    print('ID Number: ', matricula)
                    print('Money remaining: ', credito_1)
                    print('\n')
                    
                    #Atualização do banco de dados
                    conn = sqlite3.connect('Banco_de_dados.db')
                    conn.execute("UPDATE CADASTROS set RU = " +str(round(credito_1, 2))+ " WHERE  MATRICULA = "+ str(matricula));
                    conn.execute('UPDATE CADASTROS set ACESSOS = ACESSOS+1 WHERE  MATRICULA='+str(matricula));
                    conn.commit()
                    print('\n')
                    conn.close()
                    
                    c.creating_logs(nome, matricula, credito_1, credito, 1)
                                      

                    time.sleep(5)
                    #os.system("sudo ./gpio") Only used in raspberry pi tests with reley
                    Value_Increment1 = 0
                    Value_Increment2 = 0
                    time.sleep(0.1)
            
            #User doesnt have enougth money to go in
            elif(Value_Increment1 == Frames and credito_1 < 0.0):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2) #Vermelho
                id = 'Access denied...'
                                
                #Temporalização para travar a tela de monitoramento
                if(Value_Increment2 == Frames2):
                    
                    #Show in infos in console
                    print('Access denied: ', nome)
                    print('ID Number: ', matricula)
                    print('Money remening: ', credito)
                    print('\n')
                    
                    #Criando o arquivo de logs

                    
                    #Freezing face time
                    Value_Increment1 = 0
                    Value_Increment2 = 0
                    time.sleep(5)
            
            #User trying to acess to many times
            elif(Value_Increment1 == Frames and numero_acessos != 0):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,165,255), 2) #Oranje
                id = 'Access numbers expired...'
                                

                if(Value_Increment2 == Frames2):
                    
                    #Show infos in console
                    print('Access numbers expired... ', nome)
                    print('ID Number: ', matricula)
                    print('\n')

                    c.creating_logs(nome, matricula, credito_1, credito, 3)

                    #Freezing face time
                    time.sleep(5)
                    Value_Increment1 = 0
                    Value_Increment2 = 0

            #Increment security system
            else:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,255), 2) #yellow
                id = 'Identifying'
                Value_Increment1 = Value_Increment1 + 1
                
        #Under 68% showing Unknown in video
        elif (confidence < confidence_out):
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            id = 'Unknown'
            confidence = "  {0}%".format(round(100 - confidence))

        
        #Error condition = frame increment reset
        else:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
            id = 'Error'
            confidence = "  {0}%".format(round(100 - confidence))
            Value_Increment1 = 0
            Value_Increment2 = 0
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Limpar as telas quando sair

cam.release()
cv2.destroyAllWindows()
