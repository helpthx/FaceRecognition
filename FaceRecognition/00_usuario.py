''' Funções para editar as colunas do banco de dados  Créditos no RU/ Acessos
	helpthx
'''

import sqlite3
import sys
import sys, traceback
import os



def make_table():
	conn = sqlite3.connect('Banco_de_dados.db')
	print('\nDatabase open successfully...');

	conn.execute('''CREATE TABLE CADASTROS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         NOME           TEXT    NOT NULL,
         MATRICULA            INT     NOT NULL,
         RU        	REAL NOT NULL,
         ACESSOS         INT NOT NULL);''')
	conn.execute('INSERT INTO CADASTROS VALUES (0, "USUARIO 0", 00000000 , 00.00, 0)')
	conn.commit()
	print('Table criated successfully...');
	print('\n')
	conn.close()
	os.system('sudo chmod 777 Banco_de_dados.db')
	sys.exit(1)

def adding_credits():
	conn = sqlite3.connect('Banco_de_dados.db')
	print('\nDatabase open successfully...');
	
	matricula = input('Which registrations number:  ')
	dinheiro = input('Who much money do you wanna put ?: ')
	float(dinheiro)
	conn.execute("UPDATE CADASTROS set RU = RU +" +dinheiro+ " WHERE  MATRICULA = "+ matricula);
	conn.commit()
	print('\nTotal columns number updates: ', conn.total_changes)
	if conn.total_changes > 0:
		print('Change successfully...')
	else:
		print('Failed something wrong...')

	print('\n')
	#os.system('clear')
	conn.close()
	sys.exit(1)

def person_accounts():
	conn = sqlite3.connect('Banco_de_dados.db')
	print('\nDatabase open successfully...');
	print('---------------------------')
	MATRICULA1 = input('Type your registrations number: ')
	
	conn.execute('UPDATE CADASTROS set ACESSOS = ACESSOS+1 WHERE  MATRICULA='+MATRICULA1);
	conn.commit()
	print('Numero total de colunas atualizadas: ', conn.total_changes)
	if conn.total_changes > 0:
		print('Change successfully...')
	else:
		print('Failed something wrong...')

	print('\n')
	#os.system('clear')
	conn.close()
	sys.exit(1)

def loop_principal():
	print('------------------------------------------------------------------------')
	print('1 -> Table create; 2 -> Adding credits; 3 -> Access counter; 5 -> Exit: ')
	print('------------------------------------------------------------------------')
	a = input()
	x = 1

	while(x):
		if int(a) == 1:
			make_table()
			print('\nTable created successfully...')
			a = 0;

		elif int(a) == 2:
			adding_credits()
			print('\nCredit added successfully...')
			a = 0;
			
		elif int(a) == 3:
			person_accounts()
			print('\nSomeone passed...')
			a = 0;

		elif int(a) == 5:
			print('\nExiting...')
			sys.exit(0)
			
		else:
			print('\nBacking to begining')
			loop_principal()


loop_principal()
