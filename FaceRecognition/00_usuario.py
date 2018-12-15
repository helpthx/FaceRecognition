''' Funções para editar as colunas do banco de dados  Créditos no RU/ Acessos
	helpthx
'''

import sqlite3
import sys
import sys, traceback
import os
from fuctions import Enrollment_functions
c = Enrollment_functions()

def loop_principal():
	print('------------------------------------------------------------------------')
	print('1 -> Table create; 2 -> Adding credits; 3 -> Access counter; 5 -> Exit: ')
	print('------------------------------------------------------------------------')
	a = input()
	x = 1

	while(x):
		if int(a) == 1:
			c.make_table()
			print('\nTable created successfully...')
			a = 0;

		elif int(a) == 2:
			c.adding_credits()
			print('\nCredit added successfully...')
			a = 0;
			
		elif int(a) == 3:
			c.person_accounts()
			print('\nSomeone passed...')
			a = 0;

		elif int(a) == 5:
			print('\nExiting...')
			sys.exit(0)
			
		else:
			print('\nBacking to begining')
			loop_principal()


loop_principal()
