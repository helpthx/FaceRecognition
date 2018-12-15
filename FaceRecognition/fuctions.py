import numpy as np
import os
import time
from datetime import datetime
import sqlite3
import sys


class Real_time_fuctions:

    def convert_list(self):
        id_list = []
        name_list = []
        matricula_list = []
        ru_list = []
        acessos_list = []
        data = []
        conn = sqlite3.connect('Banco_de_dados.db')
        print('Database open successfully...')

        cursor = conn.execute("SELECT ID, NOME, MATRICULA, RU, ACESSOS from CADASTROS")
        for row in cursor:
            id_list.append(int(row[0]))
            name_list.append(row[1])
            matricula_list.append(int(row[2]))
            ru_list.append(float(row[3]))
            acessos_list.append(int(row[4]))

        print("Change successfully...")
        conn.close()

    def zero_reset(self):
        conn = sqlite3.connect('Banco_de_dados.db')
        print('-----------------------------')
        print('Database open successfully...')

        conn.execute('UPDATE CADASTROS set ACESSOS = 0')
        conn.commit()
        print('Total columns number updates: ', conn.total_changes)
        if conn.total_changes > 0:
            print('Change successfully...')
            print('---------------------------')
        else:
            print('Failed something wrong...')


        print('\n')
        conn.close()

    def creating_logs(self, nome, matricula, credito_1, credito, ref):
        now = datetime.now()
        arq = open('Logs/log.txt', 'a')
        data = []
        data.append('\n-------------------------\n')
        data.append("Date: ")
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
        if ref == 1:
            data.append(str('\nWelcome: ' + nome))
            data.append(str('\nID Number: ' + matricula))
            data.append('\nMoney remening: ' + str(credito_1))
            data.append('\nMoney before: ' + str(credito))
            data.append('\n------------------------\n')
        elif ref == 2:
            data.append(str('\nAccess denied: ' + nome))
            data.append(str('\nID Number: ' + matricula))
            data.append('\nMoney remening: ' + str(credito_1))
            data.append('\nMoney before: ' + str(credito))
            data.append('\n------------------------\n')
        elif ref == 3:
            data.append('\nAccess numbers expired...')
            data.append(str('\nName ' + nome))
            data.append(str('\nID Number: ' + matricula))
            data.append('\nMoney: ' + str(credito))
            data.append('\n------------------------\n')

        arq.writelines(data)
        arq.close()




